#!/usr/bin/env python3
"""Remap omitted victory points to nearest valid BSR province within each state.

Handles two cases:
1. Non-split/merge states: BSR_REVIEW commented VP entries are uncommented and remapped
2. Split/merge states: omitted VPs are re-added with remapped province IDs

Uses BSR definition.csv and provinces.bmp as the source of truth for province data.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bsr_map_tool import (
    DEFAULT_BSR_ROOT,
    PROVINCE_TOKEN_RE,
    VP_RE,
    DefinitionEntry,
    parse_states,
    read_definition,
    read_text,
    write_text,
    matching_brace,
)

STAGED_DIR = Path("tools/map_bsr/generated/staged_history/states")
GENERATED_DIR = Path("tools/map_bsr/generated")
BSR_ROOT = DEFAULT_BSR_ROOT

VP_VALUE_RE = re.compile(r"(\d+)\s+([-+]?\d+(?:\.\d+)?)")
VP_BLOCK_RE = re.compile(r"victory_points\s*=\s*\{([^}]*)\}", re.DOTALL)
BSR_REVIEW_VP_RE = re.compile(
    r"([ \t]*)#\s*BSR_REVIEW omitted invalid victory point province (\d+)"
)


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


def distance_sq(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def find_nearest_land_province(
    target_pid: int,
    valid_provinces: set[int],
    centers: dict[int, tuple[float, float]],
    definition: dict[int, DefinitionEntry],
) -> int | None:
    if target_pid not in centers:
        valid_list = list(valid_provinces)
        if valid_list:
            return valid_list[0]
        return None
    target_center = centers[target_pid]
    candidates: list[tuple[float, int]] = []
    for pid in valid_provinces:
        if pid not in centers:
            continue
        entry = definition.get(pid)
        if not entry or not entry.is_land:
            continue
        d = distance_sq(target_center, centers[pid])
        candidates.append((d, pid))
    if not candidates:
        for pid in valid_provinces:
            if pid in centers:
                candidates.append((0.0, pid))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def extract_tsr_vps(tsr_states_dir: Path) -> dict[int, list[tuple[int, float]]]:
    tsr_states = parse_states(tsr_states_dir)
    result: dict[int, list[tuple[int, float]]] = {}
    for state in tsr_states.values():
        if not state.history_block:
            continue
        vps: list[tuple[int, float]] = []
        for m in VP_BLOCK_RE.finditer(state.history_block):
            inner = m.group(1)
            for vm in VP_VALUE_RE.finditer(inner):
                prov = int(vm.group(1))
                val = float(vm.group(2))
                vps.append((prov, val))
        if vps:
            result[state.state_id] = vps
    return result


def remap_vps_in_file(
    path: Path,
    definition: dict[int, DefinitionEntry],
    centers: dict[int, tuple[float, float]],
    tsr_vp_map: dict[int, list[tuple[int, float]]],
    overlay_map: dict[str, str],
    dry_run: bool = False,
) -> tuple[int, int, list[str]]:
    text = read_text(path)
    log: list[str] = []

    state_id_match = re.search(r"\bid\s*=\s*(\d+)", text)
    if not state_id_match:
        return 0, 0, ["no state id"]
    state_id = int(state_id_match.group(1))

    tsr_id_match = re.search(r"# BSR_MAPPING tsr_state_id=(\d+)", text)
    tsr_id = int(tsr_id_match.group(1)) if tsr_id_match else None

    provinces_match = re.search(r"provinces\s*=\s*\{([^}]+)\}", text)
    if not provinces_match:
        return 0, 0, [f"state {state_id}: no provinces block"]
    valid_provinces = {int(x) for x in PROVINCE_TOKEN_RE.findall(provinces_match.group(1))}

    remapped = 0
    added = 0

    # Case 1: uncomment BSR_REVIEW VP comments and remap province
    def replace_review_vp(m: re.Match) -> str:
        nonlocal remapped
        indent = m.group(1)
        old_prov = int(m.group(2))
        # Find VP value from TSR2 source
        vp_val = 1.0
        if tsr_id and tsr_id in tsr_vp_map:
            for pv, pval in tsr_vp_map[tsr_id]:
                if pv == old_prov:
                    vp_val = pval
                    break
        new_prov = find_nearest_land_province(old_prov, valid_provinces, centers, definition)
        if new_prov is None:
            log.append(f"state {state_id}: cannot remap VP province {old_prov}, no valid provinces")
            return m.group(0)
        if new_prov != old_prov:
            log.append(f"state {state_id}: VP remapped province {old_prov} -> {new_prov} (value={vp_val})")
        else:
            log.append(f"state {state_id}: VP province {old_prov} kept")
        remapped += 1
        val_str = str(int(vp_val)) if vp_val == int(vp_val) else f"{vp_val:.1f}"
        return f"{indent}victory_points = {{\n{indent}\t\t{new_prov} {val_str}\n{indent}\t}}"

    text = BSR_REVIEW_VP_RE.sub(replace_review_vp, text)

    # Case 2: split/merge states - add omitted VPs
    mapping_type = overlay_map.get(str(state_id), "")
    if mapping_type in ("split", "merge") and tsr_id and tsr_id in tsr_vp_map:
        existing_vp_provinces: set[int] = set()
        for vm in VP_VALUE_RE.finditer(text):
            existing_vp_provinces.add(int(vm.group(1)))

        omitted_vps: list[tuple[int, float]] = []
        for prov, val in tsr_vp_map[tsr_id]:
            if prov not in valid_provinces:
                omitted_vps.append((prov, val))

        if omitted_vps:
            history_match = re.search(r"history\s*=\s*\{", text)
            if history_match:
                brace_start = text.find("{", history_match.start())
                brace_end = matching_brace(text, brace_start)
                history_block = text[brace_start + 1 : brace_end]

                vp_lines: list[str] = []
                for old_prov, val in omitted_vps:
                    new_prov = find_nearest_land_province(old_prov, valid_provinces, centers, definition)
                    if new_prov is None:
                        log.append(f"state {state_id}: cannot remap split/merge VP province {old_prov}")
                        continue
                    val_str = str(int(val)) if val == int(val) else f"{val:.1f}"
                    vp_lines.append(f"\t\t\tvictory_points = {{\n\t\t\t\t{new_prov} {val_str}\n\t\t\t}}  # BSR_REMAPPED from {old_prov}")
                    log.append(f"state {state_id}: split/merge VP added province {new_prov} (from {old_prov}, value={val})")
                    added += 1

                if vp_lines:
                    # Insert VPs before the first victory_points or after owner
                    insert_point = history_block.find("victory_points")
                    if insert_point == -1:
                        owner_match = re.search(r"owner\s*=\s*\w+", history_block)
                        if owner_match:
                            line_end = history_block.find("\n", owner_match.end())
                            insert_point = line_end + 1 if line_end != -1 else len(history_block)
                        else:
                            insert_point = 0
                    else:
                        line_start = history_block.rfind("\n", 0, insert_point) + 1
                        insert_point = line_start

                    vp_block = "\n".join(vp_lines) + "\n"
                    new_history = history_block[:insert_point] + vp_block + history_block[insert_point:]
                    text = text[:brace_start + 1] + new_history + text[brace_end:]

    if not dry_run and (remapped > 0 or added > 0):
        write_text(path, text)

    return remapped, added, log


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged-dir", type=Path, default=STAGED_DIR)
    parser.add_argument("--bsr-root", type=Path, default=BSR_ROOT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    staged_dir = args.staged_dir.resolve()
    bsr_root = args.bsr_root.resolve()
    generated_dir = GENERATED_DIR.resolve()

    print("Reading BSR definition.csv...")
    definition = read_definition(bsr_root / "map" / "definition.csv")

    print("Building province coordinate map from provinces.bmp...")
    centers = build_province_centers(bsr_root / "map" / "provinces.bmp", definition)
    print(f"  {len(centers)} province centers computed")

    print("Extracting VP data from TSR2 states...")
    tsr_vp_map = extract_tsr_vps(Path("history/states"))
    print(f"  {len(tsr_vp_map)} TSR2 states with VPs")

    overlay_map: dict[str, str] = {}
    overlay_path = generated_dir / "staged_overlay_decisions.csv"
    if overlay_path.exists():
        with overlay_path.open(newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                overlay_map[row["bsr_state_id"]] = row["selected_mapping_type"]

    # Collect all files that need VP work
    review_files: set[Path] = set()
    for path in staged_dir.glob("*.txt"):
        text = read_text(path)
        if "BSR_REVIEW omitted invalid victory point" in text:
            review_files.add(path)

    with open(generated_dir / "omitted_victory_points.csv", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            state_id = row["bsr_state_id"]
            mapping_type = overlay_map.get(state_id, "")
            if mapping_type in ("split", "merge"):
                target = staged_dir / f"{state_id}-*.txt"
                matches = list(staged_dir.glob(f"{state_id}-*.txt"))
                if matches:
                    review_files.add(matches[0])

    print(f"Processing {len(review_files)} staged state files for VP remap...")

    total_remapped = 0
    total_added = 0
    all_log: list[str] = []

    for path in sorted(review_files):
        remapped, added, log = remap_vps_in_file(
            path, definition, centers, tsr_vp_map, overlay_map, dry_run=args.dry_run
        )
        total_remapped += remapped
        total_added += added
        all_log.extend(log)

    print(f"\nResults: {total_remapped} VPs remapped (commented), {total_added} VPs added (split/merge)")
    log_path = generated_dir / "remap_victory_points.log"
    write_text(log_path, "\n".join(all_log) + "\n")
    print(f"Log written to {log_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
