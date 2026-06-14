#!/usr/bin/env python3
"""Reassign victory points using BSR as the authoritative source.

Policy:
  1. If BSR state has VPs → use BSR VPs (already valid for BSR provinces)
  2. If BSR has no VPs but TSR2 does → remap TSR2 VPs to nearest valid BSR province
  3. If neither has VPs → no VPs

Uses BSR definition.csv and provinces.bmp as the source of truth.
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
    DefinitionEntry,
    parse_states,
    read_definition,
    read_text,
    write_text,
    matching_brace,
    strip_line_comments,
)

STAGED_DIR = Path("tools/map_bsr/generated/staged_history/states")
GENERATED_DIR = Path("tools/map_bsr/generated")
BSR_ROOT = DEFAULT_BSR_ROOT

VP_BLOCK_RE = re.compile(r"victory_points\s*=\s*\{([^}]*)\}", re.DOTALL)
VP_VALUE_RE = re.compile(r"(\d+)\s+([-+]?\d+(?:\.\d+)?)")


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
        valid_list = sorted(valid_provinces)
        for pid in valid_list:
            entry = definition.get(pid)
            if entry and entry.is_land:
                return pid
        return valid_list[0] if valid_list else None
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
                candidates.append((distance_sq(target_center, centers[pid]), pid))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][1]


def extract_vps(state_map: dict[int, "StateFile"]) -> dict[int, list[tuple[int, float]]]:
    result: dict[int, list[tuple[int, float]]] = {}
    for state in state_map.values():
        if not state.history_block:
            continue
        hist = strip_line_comments(state.history_block)
        vps: list[tuple[int, float]] = []
        for m in VP_BLOCK_RE.finditer(hist):
            inner = m.group(1)
            for vm in VP_VALUE_RE.finditer(inner):
                prov = int(vm.group(1))
                val = float(vm.group(2))
                vps.append((prov, val))
        if vps:
            result[state.state_id] = vps
    return result


def remove_vp_blocks(text: str) -> tuple[str, list[str]]:
    removed: list[str] = []
    def replacer(m: re.Match) -> str:
        removed.append(m.group(0).strip())
        return ""
    result = VP_BLOCK_RE.sub(replacer, text)
    # Also remove BSR_REVIEW VP comments
    result = re.sub(r"[ \t]*#\s*BSR_REVIEW omitted invalid victory point province \d+\n?", "", result)
    result = re.sub(r"[ \t]*#\s*BSR_REMAPPED from \d+\n?", "", result)
    return result, removed


def detect_history_indent(text: str, history_start: int) -> str:
    brace_pos = text.find("{", history_start)
    first_line_start = text.find("\n", brace_pos) + 1
    line_end = text.find("\n", first_line_start)
    line = text[first_line_start:line_end] if line_end != -1 else text[first_line_start:]
    indent = ""
    for ch in line:
        if ch in " \t":
            indent += ch
        else:
            break
    return indent or "\t\t"


def format_vp_block(vps: list[tuple[int, float]], indent: str = "\t\t") -> str:
    lines: list[str] = []
    for prov, val in vps:
        val_str = str(int(val)) if val == int(val) else f"{val:.1f}"
        lines.append(f"{indent}victory_points = {{\n{indent}\t{prov} {val_str}\n{indent}}}")
    return "\n".join(lines)


def reassign_vps(
    path: Path,
    definition: dict[int, DefinitionEntry],
    centers: dict[int, tuple[float, float]],
    bsr_vp_map: dict[int, list[tuple[int, float]]],
    tsr_vp_map: dict[int, list[tuple[int, float]]],
    dry_run: bool = False,
) -> tuple[int, int, int, list[str]]:
    text = read_text(path)
    log: list[str] = []

    state_id_match = re.search(r"\bid\s*=\s*(\d+)", text)
    if not state_id_match:
        return 0, 0, 0, ["no state id"]
    state_id = int(state_id_match.group(1))

    tsr_id_match = re.search(r"# BSR_MAPPING tsr_state_id=(\d+)", text)
    tsr_id = int(tsr_id_match.group(1)) if tsr_id_match else None

    provinces_match = re.search(r"provinces\s*=\s*\{([^}]+)\}", text)
    if not provinces_match:
        return 0, 0, 0, [f"state {state_id}: no provinces"]
    valid_provinces = {int(x) for x in PROVINCE_TOKEN_RE.findall(provinces_match.group(1))}

    # Remove all existing VP entries
    cleaned, removed = remove_vp_blocks(text)

    # Determine VPs to use
    used_bsr = 0
    used_tsr_remapped = 0
    final_vps: list[tuple[int, float]] = []

    bsr_vps = bsr_vp_map.get(state_id, [])
    tsr_vps = tsr_vp_map.get(tsr_id, []) if tsr_id else []

    if bsr_vps:
        # Use BSR VPs directly
        for prov, val in bsr_vps:
            if prov in valid_provinces:
                final_vps.append((prov, val))
            else:
                new_prov = find_nearest_land_province(prov, valid_provinces, centers, definition)
                if new_prov is not None:
                    final_vps.append((new_prov, val))
                    if new_prov != prov:
                        log.append(f"state {state_id}: BSR VP {prov} -> {new_prov}")
                else:
                    log.append(f"state {state_id}: BSR VP {prov} dropped (no valid province)")
        used_bsr = len(final_vps)
    elif tsr_vps:
        # Remap TSR2 VPs to nearest BSR province
        for prov, val in tsr_vps:
            if prov in valid_provinces:
                final_vps.append((prov, val))
            else:
                new_prov = find_nearest_land_province(prov, valid_provinces, centers, definition)
                if new_prov is not None:
                    final_vps.append((new_prov, val))
                    log.append(f"state {state_id}: TSR2 VP {prov} -> {new_prov} (val={val})")
                else:
                    log.append(f"state {state_id}: TSR2 VP {prov} dropped (no valid province)")
        used_tsr_remapped = len(final_vps)

    if not final_vps:
        if not dry_run:
            write_text(path, cleaned)
        return used_bsr, used_tsr_remapped, 0, log

    # Insert VPs into history block at top level (not inside dated blocks)
    history_match = re.search(r"history\s*=\s*\{", cleaned)
    if not history_match:
        if not dry_run:
            write_text(path, cleaned)
        return used_bsr, used_tsr_remapped, 0, log

    brace_start = cleaned.find("{", history_match.start())
    brace_end = matching_brace(cleaned, brace_start)
    history_inner = cleaned[brace_start + 1 : brace_end]

    vp_block = format_vp_block(final_vps, detect_history_indent(cleaned, history_match.start())) + "\n"

    # Find top-level owner line in history (skip nested blocks)
    insert_point = 0
    depth = 0
    for line in history_inner.split("\n"):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            insert_point += len(line) + 1
            continue
        depth_change = stripped.count("{") - stripped.count("}")
        if depth == 0:
            if stripped.startswith("owner") or stripped.startswith("controller"):
                insert_point += len(line) + 1
                depth += depth_change
                continue
            elif stripped.startswith("victory_points") or stripped.startswith("buildings"):
                break
            else:
                depth += depth_change
                insert_point += len(line) + 1
                continue
        depth += depth_change
        insert_point += len(line) + 1

    # If no owner found, insert at beginning
    if insert_point == 0:
        insert_point = len(history_inner) - len(history_inner.lstrip())

    new_history = history_inner[:insert_point] + vp_block + history_inner[insert_point:]
    new_text = cleaned[:brace_start + 1] + new_history + cleaned[brace_end:]

    if not dry_run:
        write_text(path, new_text)

    return used_bsr, used_tsr_remapped, len(final_vps), log


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

    print("Parsing BSR state files...")
    bsr_states = parse_states(bsr_root / "history" / "states")
    bsr_vp_map = extract_vps(bsr_states)
    print(f"  BSR states with VPs: {len(bsr_vp_map)}")

    print("Parsing TSR2 state files...")
    tsr_states = parse_states(Path("history/states"))
    tsr_vp_map = extract_vps(tsr_states)
    print(f"  TSR2 states with VPs: {len(tsr_vp_map)}")

    staged_files = sorted(staged_dir.glob("*.txt"))
    print(f"Processing {len(staged_files)} staged state files...")

    total_bsr = 0
    total_tsr = 0
    total_vp_count = 0
    all_log: list[str] = []

    for path in staged_files:
        used_bsr, used_tsr, vp_count, log = reassign_vps(
            path, definition, centers, bsr_vp_map, tsr_vp_map, dry_run=args.dry_run
        )
        total_bsr += used_bsr
        total_tsr += used_tsr
        total_vp_count += vp_count
        all_log.extend(log)

    print(f"\nResults: {total_vp_count} total VPs")
    print(f"  From BSR: {total_bsr}")
    print(f"  From TSR2 (remapped): {total_tsr}")
    print(f"  States with no VPs: {len(staged_files) - total_bsr - total_tsr + (total_bsr + total_tsr - total_vp_count)}")

    log_path = generated_dir / "reassign_victory_points.log"
    write_text(log_path, "\n".join(all_log) + "\n")
    print(f"Log: {log_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
