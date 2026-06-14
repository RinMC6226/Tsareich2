#!/usr/bin/env python3
"""Remap province building province IDs from TSR2 to BSR in staged state files.

For each province building that references a province not in its BSR state:
1. If the province is non-land in BSR (sea/lake), remove the building.
2. Otherwise, find the nearest valid province within the same BSR state
   (preferring coastal provinces for naval buildings).
"""

from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bsr_map_tool import (
    DEFAULT_BSR_ROOT,
    PROVINCE_BUILDING_RE,
    PROVINCE_TOKEN_RE,
    GLOBAL_BUILDING_RE,
    KNOWN_GLOBAL_BUILDINGS,
    KNOWN_PROVINCE_BUILDINGS,
    DefinitionEntry,
    matching_brace,
    parse_states,
    read_definition,
    read_text,
    write_text,
)

STAGED_DIR = Path("tools/map_bsr/generated/staged_history/states")
BSR_ROOT = DEFAULT_BSR_ROOT


def build_province_centers(bmp_path: Path, definition: dict[int, DefinitionEntry]) -> dict[int, tuple[float, float]]:
    from PIL import Image

    img = Image.open(bmp_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()

    color_to_id: dict[tuple[int, int, int], int] = {}
    for entry in definition.values():
        parts = entry.raw.split(";")
        if len(parts) >= 3:
            r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
            color_to_id[(r, g, b)] = entry.province_id

    sums: dict[int, list[float]] = {}
    counts: dict[int, int] = {}
    target_ids = set(definition.keys())

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            pid = color_to_id.get((r, g, b))
            if pid is not None and pid in target_ids:
                s = sums.setdefault(pid, [0.0, 0.0])
                s[0] += x
                s[1] += y
                counts[pid] = counts.get(pid, 0) + 1

    centers: dict[int, tuple[float, float]] = {}
    for pid, s in sums.items():
        c = counts[pid]
        centers[pid] = (s[0] / c, s[1] / c)
    return centers


def distance(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


COASTAL_BUILDINGS = {"naval_base", "coastal_bunker", "naval_supply_hub"}


def find_nearest_province(
    target_pid: int,
    valid_provinces: set[int],
    centers: dict[int, tuple[float, float]],
    definition: dict[int, DefinitionEntry],
    building_names: set[str],
) -> int | None:
    if target_pid not in centers:
        return None
    target_center = centers[target_pid]
    need_coastal = bool(building_names & COASTAL_BUILDINGS)

    candidates: list[tuple[float, int]] = []
    for pid in valid_provinces:
        if pid not in centers:
            continue
        entry = definition.get(pid)
        if not entry or not entry.is_land:
            continue
        if need_coastal and entry.is_coastal != "true":
            continue
        d = distance(target_center, centers[pid])
        candidates.append((d, pid))

    if not candidates and need_coastal:
        for pid in valid_provinces:
            if pid not in centers:
                continue
            entry = definition.get(pid)
            if not entry or not entry.is_land:
                continue
            d = distance(target_center, centers[pid])
            candidates.append((d, pid))

    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def remap_state_file(
    path: Path,
    definition: dict[int, DefinitionEntry],
    centers: dict[int, tuple[float, float]],
    dry_run: bool = False,
) -> tuple[int, int, list[str]]:
    text = read_text(path)
    state = parse_states(path.parent)[list(parse_states(path.parent).keys())[0]] if False else None

    state_id_match = re.search(r"\bid\s*=\s*(\d+)", text)
    if not state_id_match:
        return 0, 0, ["no state id found"]
    state_id = int(state_id_match.group(1))

    provinces_match = re.search(r"provinces\s*=\s*\{([^}]+)\}", text)
    if not provinces_match:
        return 0, 0, ["no provinces block"]
    valid_provinces = {int(x) for x in PROVINCE_TOKEN_RE.findall(provinces_match.group(1))}

    remapped = 0
    removed = 0
    log: list[str] = []

    output_parts: list[str] = []
    cursor = 0
    work_text = text

    buildings_match = re.search(r"buildings\s*=\s*\{", work_text)
    if not buildings_match:
        return 0, 0, []

    buildings_start = buildings_match.start()
    brace_start = work_text.find("{", buildings_start)
    brace_end = matching_brace(work_text, brace_start)

    before = work_text[:buildings_start]
    buildings_block = work_text[brace_start + 1 : brace_end]
    after = work_text[brace_end + 1 :]

    new_building_lines: list[str] = []
    building_lines = buildings_block.split("\n")

    i = 0
    while i < len(building_lines):
        line = building_lines[i]
        stripped = line.strip()

        prov_match = re.match(r"^(\s*)(\d+)\s*=\s*\{", stripped)
        if prov_match:
            indent = prov_match.group(1)
            prov_id = int(prov_match.group(2))
            open_pos = stripped.find("{")
            inner_lines: list[str] = [line]

            if open_pos != -1:
                depth = 1
                j = i + 1
                while j < len(building_lines) and depth > 0:
                    inner = building_lines[j]
                    depth += inner.count("{") - inner.count("}")
                    inner_lines.append(inner)
                    j += 1

            inner_text = "\n".join(inner_lines)
            building_names_in_block = set()
            for bm in GLOBAL_BUILDING_RE.finditer(inner_text):
                if bm.group(1) in KNOWN_PROVINCE_BUILDINGS:
                    building_names_in_block.add(bm.group(1))

            if prov_id in valid_provinces:
                entry = definition.get(prov_id)
                if entry and not entry.is_land:
                    new_building_lines.append(
                        f"{indent}\t# BSR_REVIEW removed: province {prov_id} is not land in BSR"
                    )
                    removed += 1
                    log.append(f"state {state_id}: removed building at province {prov_id} (not land)")
                else:
                    clean = re.sub(r"\s*#\s*BSR_REVIEW province id needs remap", "", inner_text)
                    new_building_lines.append(clean)
                i += len(inner_lines)
                continue

            entry = definition.get(prov_id)
            if entry and not entry.is_land:
                new_building_lines.append(
                    f"{indent}\t# BSR_REVIEW removed: province {prov_id} is {entry.terrain_type} in BSR"
                )
                removed += 1
                log.append(f"state {state_id}: removed building at province {prov_id} ({entry.terrain_type})")
                i += len(inner_lines)
                continue

            replacement = find_nearest_province(
                prov_id, valid_provinces, centers, definition, building_names_in_block
            )
            if replacement is not None:
                clean = re.sub(r"\s*#\s*BSR_REVIEW province id needs remap", "", inner_text)
                replaced = re.sub(
                    r"^\s*" + str(prov_id) + r"\s*=\s*\{",
                    f"{indent}{replacement} = {{  # BSR_REMAPPED from {prov_id}",
                    clean,
                )
                new_building_lines.append(replaced)
                remapped += 1
                log.append(f"state {state_id}: remapped province {prov_id} -> {replacement}")
            else:
                new_building_lines.append(
                    f"{indent}\t# BSR_REVIEW no valid replacement for province {prov_id}"
                )
                removed += 1
                log.append(f"state {state_id}: no replacement for province {prov_id}")
            i += len(inner_lines)
            continue

        new_building_lines.append(line)
        i += 1

    new_text = before + "buildings = {\n" + "\n".join(new_building_lines) + "\n\t}" + after

    if not dry_run and (remapped > 0 or removed > 0):
        write_text(path, new_text)

    return remapped, removed, log


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged-dir", type=Path, default=STAGED_DIR)
    parser.add_argument("--bsr-root", type=Path, default=BSR_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    staged_dir = args.staged_dir.resolve()
    bsr_root = args.bsr_root.resolve()

    print("Reading BSR definition.csv...")
    definition = read_definition(bsr_root / "map" / "definition.csv")

    print("Building province coordinate map from provinces.bmp...")
    centers = build_province_centers(bsr_root / "map" / "provinces.bmp", definition)
    print(f"  {len(centers)} province centers computed")

    review_files = []
    for path in sorted(staged_dir.glob("*.txt")):
        text = read_text(path)
        if "BSR_REVIEW province id needs remap" in text:
            review_files.append(path)

    print(f"Found {len(review_files)} staged state files with BSR_REVIEW markers")

    total_remapped = 0
    total_removed = 0
    all_log: list[str] = []

    for path in review_files:
        remapped, removed, log = remap_state_file(
            path, definition, centers, dry_run=args.dry_run
        )
        total_remapped += remapped
        total_removed += removed
        all_log.extend(log)

    print(f"\nResults: {total_remapped} remapped, {total_removed} removed")
    if all_log:
        log_path = staged_dir.parent.parent / "remap_province_buildings.log"
        write_text(log_path, "\n".join(all_log) + "\n")
        print(f"Log written to {log_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
