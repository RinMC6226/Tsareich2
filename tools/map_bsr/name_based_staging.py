#!/usr/bin/env python3
"""Stage BSR states with TSR2 overlay using name-based mapping.

Policy:
  - BSR is the source of truth for: geography, provinces, province buildings, VPs
  - TSR2 overlay provides: political data (owner/controller/cores), global buildings,
    manpower, state_category, resources, custom script content
  - Matching is done via STATE_NNN names (vanilla localisation bridge)
  - For split states (one TSR2 → multiple BSR): distribute proportionally by province count
"""

from __future__ import annotations

import csv
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

sys_path_hack = str(Path(__file__).resolve().parent)
import sys

if sys_path_hack not in sys.path:
    sys.path.insert(0, sys_path_hack)

from bsr_map_tool import (
    DEFAULT_BSR_ROOT,
    PROVINCE_TOKEN_RE,
    GLOBAL_BUILDING_RE,
    KNOWN_GLOBAL_BUILDINGS,
    KNOWN_PROVINCE_BUILDINGS,
    VP_RE,
    OWNER_RE,
    CONTROLLER_RE,
    CORE_RE,
    MANPOWER_RE,
    RESOURCE_ITEM_RE,
    strip_line_comments,
    parse_states,
    read_definition,
    read_text,
    write_text,
    matching_brace,
    find_assignment_span,
    top_level_spans,
    normalize_name,
    StateFile,
    write_csv,
)

STAGED_DIR = Path("tools/map_bsr/generated/staged_history/states")
GENERATED_DIR = Path("tools/map_bsr/generated")
BSR_ROOT = DEFAULT_BSR_ROOT
VANILLA_LOC = Path(
    "/Users/eightman/Library/Application Support/Steam/steamapps/common/"
    "Hearts of Iron IV/localisation/english"
)


def load_vanilla_state_loc() -> dict[str, str]:
    result: dict[str, str] = {}
    path = VANILLA_LOC / "state_names_l_english.yml"
    if not path.exists():
        return result
    with path.open(encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r'\s*(STATE_\d+):\s*"([^"]+)"', line)
            if m:
                result[m.group(1)] = m.group(2)
    return result


def load_vanilla_vp_loc() -> dict[int, str]:
    result: dict[int, str] = {}
    path = VANILLA_LOC / "victory_points_l_english.yml"
    if not path.exists():
        return result
    with path.open(encoding="utf-8-sig") as f:
        for line in f:
            m = re.match(r'\s*VICTORY_POINTS_(\d+):\s*"([^"]+)"', line)
            if m:
                result[int(m.group(1))] = m.group(2)
    return result


def build_name_mapping(
    bsr_states: dict[int, StateFile],
    tsr_states: dict[int, StateFile],
) -> dict[str, list[int]]:
    """Map STATE_NNN name -> list of BSR state IDs."""
    name_to_bsr: dict[str, list[int]] = {}
    for s in bsr_states.values():
        name_to_bsr.setdefault(s.state_name, []).append(s.state_id)
    return name_to_bsr


def parse_global_buildings(history_block: str) -> dict[str, int]:
    buildings: dict[str, int] = {}
    clean = strip_line_comments(history_block)
    buildings_span = find_assignment_span(clean, "buildings")
    if not buildings_span:
        return buildings
    block = clean[buildings_span[0] : buildings_span[1]]
    for m in GLOBAL_BUILDING_RE.finditer(strip_line_comments(block)):
        name = m.group(1)
        if name in KNOWN_GLOBAL_BUILDINGS:
            buildings[name] = int(m.group(2))
    return buildings


def parse_manpower(top_blocks: dict[str, list[str]]) -> int | None:
    for block in top_blocks.get("manpower", []):
        m = MANPOWER_RE.search(block)
        if m:
            return int(m.group(1))
    return None


def parse_resources(top_blocks: dict[str, list[str]]) -> dict[str, float]:
    result: dict[str, float] = {}
    for block in top_blocks.get("resources", []):
        for m in RESOURCE_ITEM_RE.finditer(strip_line_comments(block)):
            result[m.group(1)] = float(m.group(2))
    return result


def parse_political(state: StateFile) -> tuple[str, str, set[str], str]:
    if not state.history_block:
        return "", "", set(), ""
    hist = strip_line_comments(state.history_block)
    owner_m = OWNER_RE.search(hist)
    ctrl_m = CONTROLLER_RE.search(hist)
    cores = set(CORE_RE.findall(hist))
    return (
        owner_m.group(1) if owner_m else "",
        ctrl_m.group(1) if ctrl_m else "",
        cores,
        hist,
    )


def extract_non_building_history(history_block: str) -> list[str]:
    """Extract all history content except buildings block."""
    if not history_block:
        return []
    lines: list[str] = []
    clean = strip_line_comments(history_block)
    buildings_span = find_assignment_span(clean, "buildings")
    if buildings_span:
        lines.append(clean[: buildings_span[0]])
        lines.append(clean[buildings_span[1] :])
    else:
        lines.append(clean)
    return lines


def distribute_value(value: int, ratio: float) -> int:
    if value <= 0:
        return 0
    return max(1, round(value * ratio))


def render_staged_state(
    bsr: StateFile,
    tsr: StateFile | None,
    ratio: float,
    is_split: bool,
) -> tuple[str, list[str]]:
    """Render a staged state file."""
    issues: list[str] = []
    lines = [
        "state={",
        f"\tid={bsr.state_id}",
        f'\tname="{bsr.state_name}" # {bsr.display_name}',
    ]

    if tsr:
        lines.append(f"\t# TSR2_OVERLAY tsr_state_id={tsr.state_id} ratio={ratio:.3f} split={is_split}")
    else:
        lines.append("\t# TSR2_OVERLAY none (BSR-only state)")

    # Top-level blocks from BSR: state_category, impassable, local_supplies
    for key in ["state_category", "impassable", "local_supplies"]:
        for block in bsr.top_blocks.get(key, []):
            lines.append("")
            lines.extend("\t" + l if l else "" for l in block.splitlines())

    # Manpower: TSR2 if available, distributed by ratio
    bsr_mp = parse_manpower(bsr.top_blocks)
    if tsr:
        tsr_mp = parse_manpower(tsr.top_blocks)
        if tsr_mp is not None:
            dist_mp = distribute_value(tsr_mp, ratio) if is_split else tsr_mp
            lines.append(f"\n\tmanpower={dist_mp}")
        elif bsr_mp is not None:
            lines.append(f"\n\tmanpower={bsr_mp}")
    elif bsr_mp is not None:
        lines.append(f"\n\tmanpower={bsr_mp}")

    # Resources: TSR2 if available, distributed by ratio
    bsr_res = parse_resources(bsr.top_blocks)
    tsr_res = parse_resources(tsr.top_blocks) if tsr else {}
    final_res: dict[str, float] = {}
    if tsr_res:
        for name, val in tsr_res.items():
            dist = max(0, round(val * ratio)) if is_split else val
            if dist > 0:
                final_res[name] = float(dist)
    elif bsr_res:
        final_res = bsr_res

    if final_res:
        lines.append("\n\tresources={")
        for name, val in final_res.items():
            formatted = str(int(val)) if val == int(val) else f"{val:.3f}"
            lines.append(f"\t\t{name} = {formatted}")
        lines.append("\t}")

    # History block
    lines.append("\n\thistory={")

    # Political data from TSR2 (or BSR if no TSR2)
    if tsr:
        tsr_owner, tsr_ctrl, tsr_cores, tsr_hist = parse_political(tsr)
        bsr_owner, bsr_ctrl, bsr_cores, _ = parse_political(bsr)

        if tsr_owner:
            lines.append(f"\t\towner = {tsr_owner}")
        elif bsr_owner:
            lines.append(f"\t\towner = {bsr_owner}")

        if tsr_ctrl:
            lines.append(f"\t\tcontroller = {tsr_ctrl}")
        elif bsr_ctrl:
            lines.append(f"\t\tcontroller = {bsr_ctrl}")

        # Non-building, non-political content from TSR2 (events, modifiers, dated blocks)
        tsr_inner = _history_inner(tsr)
        tsr_extras = _extract_extras(tsr_inner)
        for extra in tsr_extras:
            for el in extra.splitlines():
                lines.append(f"\t\t{el}")
    else:
        bsr_owner, bsr_ctrl, bsr_cores, _ = parse_political(bsr)
        if bsr_owner:
            lines.append(f"\t\towner = {bsr_owner}")
        if bsr_ctrl:
            lines.append(f"\t\tcontroller = {bsr_ctrl}")

    # VPs: from BSR (province IDs are BSR-valid)
    if bsr.history_block:
        bsr_hist_clean = strip_line_comments(bsr.history_block)
        for m in VP_RE.finditer(bsr_hist_clean):
            lines.append(f"\t\t{m.group(0)}")

    # Buildings: province buildings from BSR, global buildings from TSR2
    # Province buildings (BSR)
    bsr_prov_buildings = _extract_province_buildings(bsr)
    if bsr_prov_buildings:
        pass  # will be added inside buildings block

    # Global buildings (TSR2, distributed)
    tsr_global = parse_global_buildings(tsr.history_block) if tsr and tsr.history_block else {}
    bsr_global = parse_global_buildings(bsr.history_block) if bsr.history_block else {}

    final_global: dict[str, int] = {}
    if tsr_global:
        for name in KNOWN_GLOBAL_BUILDINGS:
            if name in tsr_global:
                val = tsr_global[name]
                final_global[name] = distribute_value(val, ratio) if is_split else val
    elif bsr_global:
        final_global = bsr_global

    if final_global or bsr_prov_buildings:
        lines.append("\t\tbuildings = {")
        for name in KNOWN_GLOBAL_BUILDINGS:
            if name in final_global:
                lines.append(f"\t\t\t{name} = {final_global[name]}")
        # Province buildings from BSR
        for pb in bsr_prov_buildings:
            lines.extend(f"\t\t{l}" for l in pb.splitlines())
        lines.append("\t\t}")

    # Cores: merge TSR2 and BSR cores
    all_cores: set[str] = set()
    if tsr:
        _, _, tsr_cores_set, _ = parse_political(tsr)
        all_cores.update(tsr_cores_set)
    _, _, bsr_cores_set, _ = parse_political(bsr)
    all_cores.update(bsr_cores_set)
    for core in sorted(all_cores):
        lines.append(f"\t\tadd_core_of = {core}")

    # Claims from BSR
    if bsr.history_block:
        for m in re.finditer(r"\badd_claim_of\s*=\s*([A-Z0-9_]+)", strip_line_comments(bsr.history_block)):
            lines.append(f"\t\tadd_claim_of = {m.group(1)}")
    if tsr and tsr.history_block:
        for m in re.finditer(r"\badd_claim_of\s*=\s*([A-Z0-9_]+)", strip_line_comments(tsr.history_block)):
            tag = m.group(1)
            if tag not in all_cores:
                lines.append(f"\t\tadd_claim_of = {tag}")

    lines.append("\t}")

    # Provinces from BSR
    lines.append("")
    lines.extend("\t" + l if l else "" for l in bsr.province_block.splitlines())
    lines.append("}")
    lines.append("")

    return "\n".join(lines), issues


def _extract_province_buildings(state: StateFile) -> list[str]:
    if not state.history_block:
        return []
    clean = strip_line_comments(state.history_block)
    buildings_span = find_assignment_span(clean, "buildings")
    if not buildings_span:
        return []
    block = clean[buildings_span[0] : buildings_span[1]]
    results: list[str] = []
    for m in re.finditer(r"(\d+)\s*=\s*\{", block):
        prov = int(m.group(1))
        open_idx = block.find("{", m.start())
        close_idx = matching_brace(block, open_idx) + 1
        inner = block[open_idx + 1 : close_idx - 1].strip()
        if inner:
            results.append(f"{prov} = {{{inner}}}")
    return results


def _history_inner(state: StateFile) -> str:
    """Get inner content of history block (between { and })."""
    if not state.history_block:
        return ""
    text = state.history_block
    open_idx = text.find("{")
    if open_idx == -1:
        return ""
    close_idx = matching_brace(text, open_idx)
    return text[open_idx + 1 : close_idx]


def _extract_extras(inner: str) -> list[str]:
    """Extract dated blocks, set_variable, add_dynamic_modifier, etc. from history inner."""
    clean = strip_line_comments(inner)
    skip_keys = {"owner", "controller", "buildings", "victory_points"}
    political_keys = {"add_core_of", "add_claim_of", "remove_core_of"}
    spans = top_level_spans(clean)
    extras: list[str] = []
    for key, span_list in spans.items():
        if key in skip_keys or key in political_keys:
            continue
        for start, end in span_list:
            block = clean[start:end].rstrip()
            if block:
                extras.append(block)
    return extras


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bsr-root", type=Path, default=BSR_ROOT)
    parser.add_argument("--out-dir", type=Path, default=GENERATED_DIR)
    args = parser.parse_args()

    bsr_root = args.bsr_root.resolve()
    out_dir = args.out_dir.resolve()
    staged_dir = out_dir / "staged_history" / "states"

    print("Loading vanilla localisation...")
    vanilla_loc = load_vanilla_state_loc()
    vanilla_vp = load_vanilla_vp_loc()
    print(f"  State names: {len(vanilla_loc)}, VP names: {len(vanilla_vp)}")

    print("Parsing BSR state files...")
    bsr_states = parse_states(bsr_root / "history" / "states")
    print(f"  {len(bsr_states)} BSR states")

    print("Parsing TSR2 state files...")
    tsr_states = parse_states(Path("history/states"))
    print(f"  {len(tsr_states)} TSR2 states")

    # Build name -> TSR2 state mapping
    name_to_tsr: dict[str, StateFile] = {}
    for s in tsr_states.values():
        name_to_tsr[s.state_name] = s

    # Build name -> BSR state IDs mapping
    name_to_bsr_ids: dict[str, list[int]] = {}
    for s in bsr_states.values():
        name_to_bsr_ids.setdefault(s.state_name, []).append(s.state_id)

    # Match and stage
    if staged_dir.exists():
        shutil.rmtree(staged_dir)
    staged_dir.mkdir(parents=True, exist_ok=True)

    mapping_rows: list[dict[str, str]] = []
    matched = 0
    bsr_only = 0
    split_count = 0

    for bsr_state_name, bsr_ids in sorted(name_to_bsr_ids.items()):
        tsr = name_to_tsr.get(bsr_state_name)
        is_split = len(bsr_ids) > 1

        # Calculate total BSR provinces for ratio
        total_bsr_provinces = sum(len(bsr_states[bid].provinces) for bid in bsr_ids)

        for bsr_id in bsr_ids:
            bsr = bsr_states[bsr_id]
            ratio = len(bsr.provinces) / max(1, total_bsr_provinces) if is_split else 1.0

            text, issues = render_staged_state(bsr, tsr, ratio, is_split)
            filename = f"{bsr_id}-{bsr.display_name.replace('/', '_')}.txt"
            write_text(staged_dir / filename, text)

            mapping_rows.append({
                "bsr_state_id": str(bsr_id),
                "bsr_state_name": bsr.display_name,
                "bsr_state_key": bsr.state_name,
                "tsr_state_id": str(tsr.state_id) if tsr else "",
                "tsr_state_name": tsr.display_name if tsr else "",
                "vanilla_english_name": vanilla_loc.get(bsr_state_name, ""),
                "is_split": str(is_split),
                "ratio": f"{ratio:.3f}",
                "bsr_province_count": str(len(bsr.provinces)),
            })

            if tsr:
                matched += 1
            else:
                bsr_only += 1

        if is_split:
            split_count += 1

    write_csv(
        out_dir / "name_based_mapping.csv",
        mapping_rows,
        ["bsr_state_id", "bsr_state_name", "bsr_state_key", "tsr_state_id",
         "tsr_state_name", "vanilla_english_name", "is_split", "ratio", "bsr_province_count"],
    )

    summary = {
        "bsr_states": len(bsr_states),
        "tsr_states": len(tsr_states),
        "matched": matched,
        "bsr_only": bsr_only,
        "split_groups": split_count,
        "unique_state_names": len(name_to_bsr_ids),
    }
    write_text(out_dir / "name_based_staging_summary.json", json.dumps(summary, indent=2) + "\n")

    print(f"\nResults:")
    print(f"  BSR states staged: {len(bsr_states)}")
    print(f"  Matched to TSR2: {matched}")
    print(f"  BSR-only: {bsr_only}")
    print(f"  Split groups: {split_count}")
    print(f"  Unique state names: {len(name_to_bsr_ids)}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
