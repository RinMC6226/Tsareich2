#!/usr/bin/env python3
"""BSR map integration helpers for Tsareich2.

The tool deliberately stages data and reports instead of replacing live map or
state files. It is meant to make every mapping decision reviewable.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_BSR_ROOT = Path("/Users/eightman/Desktop/HOI4_modding/2640808954")
DEFAULT_OUT_DIR = Path("tools/map_bsr/generated")
DEFAULT_MANUAL_DECISIONS = Path("tools/map_bsr/manual_decisions.csv")
STATE_FILE_RE = re.compile(r"^\s*state\s*=\s*\{", re.MULTILINE)
ID_RE = re.compile(r"\bid\s*=\s*(\d+)")
NAME_RE = re.compile(r'\bname\s*=\s*"([^"]+)"(?:\s*#\s*(.*))?')
ASSIGNMENT_RE = re.compile(r"^(\s*)([A-Za-z0-9_]+)\s*=", re.MULTILINE)
PROVINCE_TOKEN_RE = re.compile(r"\b\d+\b")
VP_RE = re.compile(r"\bvictory_points\s*=\s*\{\s*(\d+)\s+[-+]?\d+(?:\.\d+)?\s*\}")
PROVINCE_BUILDING_RE = re.compile(r"^\s*(\d+)\s*=\s*\{", re.MULTILINE)
OWNER_RE = re.compile(r"\bowner\s*=\s*([A-Z0-9_]+)")
CONTROLLER_RE = re.compile(r"\bcontroller\s*=\s*([A-Z0-9_]+)")
CORE_RE = re.compile(r"\badd_core_of\s*=\s*([A-Z0-9_]+)")
CONTINENT_NAMES = {
    "1": "europe",
    "2": "north_america",
    "3": "south_america",
    "4": "australia",
    "5": "africa",
    "6": "asia",
    "7": "middle_east",
}
RUSSIA_REVIEW_TAGS = {
    "RUS",
    "SOV",
    "SIB",
    "FER",
    "ALT",
    "KAZ",
    "TRK",
    "UZB",
    "TAJ",
    "KYR",
}
AUTOMATIC_MAPPING_TYPES = {
    "same_id_same_area",
    "same_name",
    "province_overlap",
    "split",
    "merge",
}
MAPPING_FIELDNAMES = [
    "tsr_state_id",
    "tsr_state_name",
    "bsr_state_id",
    "bsr_state_name",
    "mapping_type",
    "confidence",
    "notes",
]
REVIEW_DECISION_FIELDNAMES = [
    "bsr_state_id",
    "bsr_state_name",
    "bsr_continent",
    "selected_tsr_state_id",
    "selected_tsr_state_name",
    "selected_mapping_type",
    "selected_confidence",
    "alternative_mapping_count",
    "issue_count",
    "vp_omission_count",
    "manual_building_distribution",
    "manual_resource_distribution",
    "owner_core_conflict",
    "decision_status",
    "decision_reason",
    "review_categories",
    "selection_notes",
]
MANUAL_DECISION_FIELDNAMES = [
    "bsr_state_id",
    "bsr_state_name",
    "current_selected_tsr_state_id",
    "current_selected_tsr_state_name",
    "current_mapping_type",
    "suggested_decision_status",
    "manual_decision",
    "manual_tsr_state_id",
    "reviewer_notes",
]


@dataclass
class StateFile:
    path: Path
    state_id: int
    state_name: str
    display_name: str
    text: str
    body: str
    provinces: set[int]
    province_block: str
    history_block: str | None
    top_blocks: dict[str, list[str]]


@dataclass
class DefinitionEntry:
    province_id: int
    terrain_type: str
    is_coastal: str
    terrain: str
    continent: str
    raw: str

    @property
    def is_land(self) -> bool:
        return self.terrain_type == "land"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_size(path: Path) -> int:
    return path.stat().st_size


def bmp_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()[:26]
    if len(data) < 26 or data[:2] != b"BM":
        return None
    width = int.from_bytes(data[18:22], "little", signed=True)
    height = int.from_bytes(data[22:26], "little", signed=True)
    return abs(width), abs(height)


def matching_brace(text: str, open_index: int) -> int:
    depth = 0
    for idx in range(open_index, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return idx
    raise ValueError("unmatched brace")


def find_assignment_span(text: str, key: str, start: int = 0) -> tuple[int, int] | None:
    pattern = re.compile(rf"(?m)^([ \t]*){re.escape(key)}\s*=")
    match = pattern.search(text, start)
    if not match:
        return None
    value_start = match.end()
    idx = value_start
    while idx < len(text) and text[idx].isspace():
        idx += 1
    if idx < len(text) and text[idx] == "{":
        end = matching_brace(text, idx) + 1
        while end < len(text) and text[end] in " \t":
            end += 1
        if end < len(text) and text[end] == "\n":
            end += 1
        return match.start(), end
    line_end = text.find("\n", value_start)
    if line_end == -1:
        return match.start(), len(text)
    return match.start(), line_end + 1


def find_all_assignment_spans(text: str, key: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    start = 0
    while True:
        span = find_assignment_span(text, key, start)
        if not span:
            break
        spans.append(span)
        start = span[1]
    return spans


def top_level_spans(body: str) -> dict[str, list[tuple[int, int]]]:
    spans: dict[str, list[tuple[int, int]]] = {}
    idx = 0
    while idx < len(body):
        if body[idx] == "#":
            newline = body.find("\n", idx)
            idx = len(body) if newline == -1 else newline + 1
            continue
        match = ASSIGNMENT_RE.match(body, idx)
        if not match:
            idx += 1
            continue
        key = match.group(2)
        value_start = match.end()
        probe = value_start
        while probe < len(body) and body[probe].isspace():
            probe += 1
        if probe < len(body) and body[probe] == "{":
            end = matching_brace(body, probe) + 1
            while end < len(body) and body[end] in " \t":
                end += 1
            if end < len(body) and body[end] == "\n":
                end += 1
        else:
            line_end = body.find("\n", value_start)
            end = len(body) if line_end == -1 else line_end + 1
        spans.setdefault(key, []).append((match.start(), end))
        idx = end
    return spans


def parse_state_file(path: Path) -> StateFile:
    text = read_text(path)
    state_match = STATE_FILE_RE.search(text)
    if not state_match:
        raise ValueError(f"{path}: missing state={{")
    open_index = text.find("{", state_match.start())
    close_index = matching_brace(text, open_index)
    body = text[open_index + 1 : close_index]
    id_match = ID_RE.search(body)
    name_match = NAME_RE.search(body)
    province_span = find_assignment_span(body, "provinces")
    if not id_match or not name_match or not province_span:
        raise ValueError(f"{path}: missing id/name/provinces")
    province_block = body[province_span[0] : province_span[1]]
    provinces = {int(value) for value in PROVINCE_TOKEN_RE.findall(province_block)}
    history_span = find_assignment_span(body, "history")
    history_block = body[history_span[0] : history_span[1]].rstrip() if history_span else None
    spans = top_level_spans(body)
    top_blocks = {
        key: [body[start:end].rstrip() for start, end in value]
        for key, value in spans.items()
    }
    comment = (name_match.group(2) or "").strip()
    state_name = name_match.group(1)
    display_name = comment or state_name or path.stem
    return StateFile(
        path=path,
        state_id=int(id_match.group(1)),
        state_name=state_name,
        display_name=display_name,
        text=text,
        body=body,
        provinces=provinces,
        province_block=province_block.rstrip(),
        history_block=history_block,
        top_blocks=top_blocks,
    )


def strip_line_comments(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def parse_states(states_dir: Path) -> dict[int, StateFile]:
    states: dict[int, StateFile] = {}
    for path in sorted(states_dir.glob("*.txt")):
        state = parse_state_file(path)
        if state.state_id in states:
            raise ValueError(
                f"duplicate state id {state.state_id}: {states[state.state_id].path} and {path}"
            )
        states[state.state_id] = state
    return states


def normalize_name(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\bstate[_\s-]*\d+\b", "", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return " ".join(value.split())


def mapping_type_and_confidence(tsr: StateFile, bsr: StateFile) -> tuple[str, float, str]:
    overlap = len(tsr.provinces & bsr.provinces)
    denominator = max(1, min(len(tsr.provinces), len(bsr.provinces)))
    overlap_ratio = overlap / denominator
    same_display_name = normalize_name(tsr.display_name) == normalize_name(bsr.display_name)
    same_state_name = normalize_name(tsr.state_name) == normalize_name(bsr.state_name)
    same_id = tsr.state_id == bsr.state_id

    if same_id and overlap_ratio >= 0.8:
        return "same_id_same_area", round(max(0.9, overlap_ratio), 3), f"province_overlap={overlap}"
    if same_display_name and overlap_ratio >= 0.35:
        return "same_name", round(max(0.75, overlap_ratio), 3), f"province_overlap={overlap}"
    if overlap_ratio >= 0.6:
        return "province_overlap", round(overlap_ratio, 3), f"province_overlap={overlap}"
    if same_id and same_state_name:
        return "manual", 0.55, f"same numeric id/name but low province_overlap={overlap}"
    if same_display_name:
        return "manual", 0.5, f"same display name but low province_overlap={overlap}"
    return "manual", round(overlap_ratio, 3), f"low province_overlap={overlap}"


def political_tags(state: StateFile) -> set[str]:
    owner, controller, cores = history_political_values(state)
    return {value for value in {owner, controller, *cores} if value}


def mapping_candidate_compatible(tsr: StateFile, bsr: StateFile) -> bool:
    if tsr.state_id == bsr.state_id:
        return True
    if normalize_name(tsr.display_name) and normalize_name(tsr.display_name) == normalize_name(bsr.display_name):
        return True
    if normalize_name(tsr.state_name) and normalize_name(tsr.state_name) == normalize_name(bsr.state_name):
        return True
    return bool(political_tags(tsr) & political_tags(bsr))


def best_mapping(
    tsr: StateFile,
    bsr_by_id: dict[int, StateFile],
    bsr_by_norm: dict[str, list[StateFile]],
    accepted_overlaps: list[tuple[int, int]],
) -> tuple[StateFile | None, str, float, str]:
    candidates: dict[int, StateFile] = {}
    if tsr.state_id in bsr_by_id:
        candidates[tsr.state_id] = bsr_by_id[tsr.state_id]
    for value in bsr_by_norm.get(normalize_name(tsr.display_name), []):
        candidates[value.state_id] = value
    for bsr_state_id, _overlap in accepted_overlaps:
        candidates[bsr_state_id] = bsr_by_id[bsr_state_id]

    if not candidates:
        return None, "retired_tsr_state", 0.0, "no same id/name/province overlap"

    scored: list[tuple[float, int, StateFile, str, str]] = []
    for bsr in candidates.values():
        mapping_type, confidence, notes = mapping_type_and_confidence(tsr, bsr)
        overlap = len(tsr.provinces & bsr.provinces)
        same_id_bonus = 0.25 if tsr.state_id == bsr.state_id else 0.0
        same_name_bonus = 0.15 if normalize_name(tsr.display_name) == normalize_name(bsr.display_name) else 0.0
        score = confidence + same_id_bonus + same_name_bonus + (overlap / 10000)
        scored.append((score, overlap, bsr, mapping_type, notes))
    scored.sort(key=lambda item: (item[0], item[1]), reverse=True)
    _, _, bsr, mapping_type, notes = scored[0]
    if scored[0][0] - scored[1][0] < 0.05 if len(scored) > 1 else False:
        mapping_type = "manual"
        notes += "; close candidate tie"
    _, confidence, _ = mapping_type_and_confidence(tsr, bsr)
    return bsr, mapping_type, confidence, notes


def add_mapping_row(
    rows: list[dict[str, str]],
    tsr: StateFile | None,
    bsr: StateFile | None,
    mapping_type: str,
    confidence: float,
    notes: str,
) -> None:
    rows.append(
        {
            "tsr_state_id": str(tsr.state_id) if tsr else "",
            "tsr_state_name": tsr.display_name if tsr else "",
            "bsr_state_id": str(bsr.state_id) if bsr else "",
            "bsr_state_name": bsr.display_name if bsr else "",
            "mapping_type": mapping_type,
            "confidence": f"{confidence:.3f}",
            "notes": notes,
        }
    )


def overlap_confidence(tsr: StateFile, bsr: StateFile, overlap: int) -> float:
    if overlap <= 0:
        return 0.0
    tsr_ratio = overlap / max(1, len(tsr.provinces))
    bsr_ratio = overlap / max(1, len(bsr.provinces))
    return round(max(tsr_ratio, bsr_ratio), 3)


def build_mapping(tsr_states: dict[int, StateFile], bsr_states: dict[int, StateFile]) -> list[dict[str, str]]:
    bsr_by_norm: dict[str, list[StateFile]] = {}
    for bsr in bsr_states.values():
        bsr_by_norm.setdefault(normalize_name(bsr.display_name), []).append(bsr)

    raw_overlaps_by_tsr: dict[int, list[tuple[int, int]]] = {state_id: [] for state_id in tsr_states}
    raw_overlaps_by_bsr: dict[int, list[tuple[int, int]]] = {state_id: [] for state_id in bsr_states}
    province_to_bsr: dict[int, int] = {}
    for bsr in bsr_states.values():
        for province in bsr.provinces:
            province_to_bsr[province] = bsr.state_id
    for tsr in tsr_states.values():
        counts: dict[int, int] = {}
        for province in tsr.provinces:
            bsr_state_id = province_to_bsr.get(province)
            if bsr_state_id is not None:
                counts[bsr_state_id] = counts.get(bsr_state_id, 0) + 1
        for bsr_state_id, overlap in counts.items():
            raw_overlaps_by_tsr[tsr.state_id].append((bsr_state_id, overlap))
            raw_overlaps_by_bsr[bsr_state_id].append((tsr.state_id, overlap))
    for values in raw_overlaps_by_tsr.values():
        values.sort(key=lambda item: item[1], reverse=True)
    for values in raw_overlaps_by_bsr.values():
        values.sort(key=lambda item: item[1], reverse=True)

    overlaps_by_tsr: dict[int, list[tuple[int, int]]] = {state_id: [] for state_id in tsr_states}
    overlaps_by_bsr: dict[int, list[tuple[int, int]]] = {state_id: [] for state_id in bsr_states}
    rejected_overlaps_by_tsr: dict[int, list[tuple[int, int]]] = {state_id: [] for state_id in tsr_states}
    for tsr_state_id, values in raw_overlaps_by_tsr.items():
        tsr = tsr_states[tsr_state_id]
        for bsr_state_id, overlap in values:
            bsr = bsr_states[bsr_state_id]
            if mapping_candidate_compatible(tsr, bsr):
                overlaps_by_tsr[tsr_state_id].append((bsr_state_id, overlap))
                overlaps_by_bsr[bsr_state_id].append((tsr_state_id, overlap))
            else:
                rejected_overlaps_by_tsr[tsr_state_id].append((bsr_state_id, overlap))
    for values in overlaps_by_tsr.values():
        values.sort(key=lambda item: item[1], reverse=True)
    for values in overlaps_by_bsr.values():
        values.sort(key=lambda item: item[1], reverse=True)

    rows: list[dict[str, str]] = []
    mapped_bsr_ids: set[int] = set()
    for tsr in sorted(tsr_states.values(), key=lambda item: item.state_id):
        for bsr_state_id, overlap in rejected_overlaps_by_tsr.get(tsr.state_id, []):
            bsr = bsr_states[bsr_state_id]
            add_mapping_row(
                rows,
                tsr,
                bsr,
                "manual",
                overlap_confidence(tsr, bsr, overlap),
                (
                    "incompatible province overlap rejected for automatic overlay; "
                    f"province_overlap={overlap}; tsr_tags={' '.join(sorted(political_tags(tsr)))}; "
                    f"bsr_tags={' '.join(sorted(political_tags(bsr)))}"
                ),
            )
        overlap_targets = overlaps_by_tsr.get(tsr.state_id, [])
        if len(overlap_targets) > 1:
            for bsr_state_id, overlap in overlap_targets:
                bsr = bsr_states[bsr_state_id]
                mapped_bsr_ids.add(bsr.state_id)
                bsr_sources = overlaps_by_bsr.get(bsr.state_id, [])
                mapping_type = "merge" if len(bsr_sources) > 1 else "split"
                if len(bsr_sources) > 1 and len(overlap_targets) > 1:
                    notes_type = "split+merge"
                else:
                    notes_type = mapping_type
                add_mapping_row(
                    rows,
                    tsr,
                    bsr,
                    mapping_type,
                    overlap_confidence(tsr, bsr, overlap),
                    (
                        f"{notes_type}; province_overlap={overlap}; "
                        f"tsr_overlap_rank={overlap_targets.index((bsr_state_id, overlap)) + 1}/{len(overlap_targets)}; "
                        f"bsr_source_count={len(bsr_sources)}"
                    ),
                )
            continue

        bsr, mapping_type, confidence, notes = best_mapping(tsr, bsr_states, bsr_by_norm, overlap_targets)
        if bsr:
            mapped_bsr_ids.add(bsr.state_id)
            bsr_sources = overlaps_by_bsr.get(bsr.state_id, [])
            if len(bsr_sources) > 1:
                mapping_type = "merge"
                overlap = len(tsr.provinces & bsr.provinces)
                confidence = overlap_confidence(tsr, bsr, overlap)
                notes = f"merge; province_overlap={overlap}; bsr_source_count={len(bsr_sources)}"
            add_mapping_row(rows, tsr, bsr, mapping_type, confidence, notes)
        else:
            add_mapping_row(
                rows,
                tsr,
                None,
                mapping_type,
                confidence,
                notes,
            )

    for bsr in sorted(bsr_states.values(), key=lambda item: item.state_id):
        if bsr.state_id not in mapped_bsr_ids:
            add_mapping_row(
                rows,
                None,
                bsr,
                "new_bsr_state",
                1.0,
                "no TSR state mapped to this BSR state",
            )
    return rows


def read_mapping(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_definition(path: Path) -> dict[int, DefinitionEntry]:
    entries: dict[int, DefinitionEntry] = {}
    with path.open(encoding="utf-8-sig", errors="replace", newline="") as f:
        for line_number, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(";")
            if len(parts) < 8:
                raise ValueError(f"{path}:{line_number}: expected at least 8 semicolon fields")
            province_id = int(parts[0])
            entries[province_id] = DefinitionEntry(
                province_id=province_id,
                terrain_type=parts[4],
                is_coastal=parts[5],
                terrain=parts[6],
                continent=parts[7],
                raw=line,
            )
    return entries


def extract_state_ids_from_filename(path: Path) -> int | None:
    match = re.match(r"^\s*(\d+)", path.name)
    return int(match.group(1)) if match else None


def snapshot(repo_root: Path, bsr_root: Path, out_dir: Path) -> None:
    targets = [
        ("tsr", repo_root / "map" / "provinces.bmp"),
        ("tsr", repo_root / "map" / "definition.csv"),
        ("bsr", bsr_root / "map" / "provinces.bmp"),
        ("bsr", bsr_root / "map" / "definition.csv"),
    ]
    rows: list[dict[str, str]] = []
    for side, path in targets:
        row = {
            "side": side,
            "path": str(path),
            "exists": str(path.exists()),
            "bytes": "",
            "sha256": "",
            "bmp_width": "",
            "bmp_height": "",
            "line_count": "",
        }
        if path.exists():
            row["bytes"] = str(file_size(path))
            row["sha256"] = sha256(path)
            size = bmp_size(path) if path.suffix.lower() == ".bmp" else None
            if size:
                row["bmp_width"], row["bmp_height"] = str(size[0]), str(size[1])
            if path.suffix.lower() == ".csv":
                row["line_count"] = str(sum(1 for _ in path.open(errors="replace")))
        rows.append(row)

    for side, root in [("tsr", repo_root), ("bsr", bsr_root)]:
        state_dir = root / "history" / "states"
        files = sorted(state_dir.glob("*.txt"))
        rows.append(
            {
                "side": side,
                "path": str(state_dir),
                "exists": str(state_dir.exists()),
                "bytes": "",
                "sha256": "",
                "bmp_width": "",
                "bmp_height": "",
                "line_count": str(len(files)),
            }
        )
    write_csv(
        out_dir / "input_snapshot.csv",
        rows,
        ["side", "path", "exists", "bytes", "sha256", "bmp_width", "bmp_height", "line_count"],
    )


def collect_mapping_reports(rows: list[dict[str, str]], out_dir: Path) -> None:
    by_type: dict[str, int] = {}
    for row in rows:
        by_type[row["mapping_type"]] = by_type.get(row["mapping_type"], 0) + 1
    write_text(out_dir / "mapping_summary.json", json.dumps(by_type, indent=2, sort_keys=True) + "\n")

    review_rows = [
        row
        for row in rows
        if row["mapping_type"] in {"manual", "split", "merge", "retired_tsr_state", "new_bsr_state"}
        or float(row["confidence"] or 0) < 0.75
    ]
    write_csv(
        out_dir / "manual_review_mappings.csv",
        review_rows,
        MAPPING_FIELDNAMES,
    )
    write_csv(
        out_dir / "retired_tsr_states.csv",
        [row for row in rows if row["mapping_type"] == "retired_tsr_state"],
        MAPPING_FIELDNAMES,
    )
    write_csv(
        out_dir / "new_bsr_states.csv",
        [row for row in rows if row["mapping_type"] == "new_bsr_state"],
        MAPPING_FIELDNAMES,
    )
    write_csv(
        out_dir / "rejected_overlap_mappings.csv",
        [row for row in rows if row["notes"].startswith("incompatible province overlap rejected")],
        MAPPING_FIELDNAMES,
    )


def state_filename(state: StateFile) -> str:
    return state.path.name


def remap_history_for_bsr(tsr: StateFile, bsr: StateFile, mapping_type: str = "") -> tuple[str | None, list[str]]:
    if not tsr.history_block:
        return None, ["missing TSR history block"]
    issues: list[str] = []
    valid_bsr_provinces = bsr.provinces

    if mapping_type in {"split", "merge"}:
        return split_merge_history_for_bsr(tsr, bsr, mapping_type)

    def vp_repl(match: re.Match[str]) -> str:
        province = int(match.group(1))
        if province not in valid_bsr_provinces:
            issues.append(f"victory_points province {province} not in BSR state {bsr.state_id}")
            return f"# BSR_REVIEW omitted invalid victory point province {province}"
        return match.group(0)

    history = VP_RE.sub(vp_repl, tsr.history_block)
    history = omit_invalid_province_buildings(history, valid_bsr_provinces, bsr.state_id, issues)
    return history, issues


INFRA_RE = re.compile(r"infrastructure\s*=\s*([0-9]+)")
GLOBAL_BUILDING_RE = re.compile(r"^\s*(\w+)\s*=\s*([0-9]+)", re.MULTILINE)

KNOWN_GLOBAL_BUILDINGS = frozenset({
    "infrastructure", "arms_factory", "industrial_complex", "dockyard",
    "air_base", "anti_air_building", "radar_station", "fuel_silo",
    "synthetic_refinery", "land_facility",
})

KNOWN_PROVINCE_BUILDINGS = frozenset({
    "naval_base", "bunker", "coastal_bunker", "naval_supply_hub",
    "radar_station", "anti_air_building", "land_facility",
})


def distribute_buildings(
    bldg_text: str, ratio: float, valid_provinces: set[int], bsr_state_id: int, issues: list[str],
) -> str | None:
    global_buildings: dict[str, int] = {}
    for m in GLOBAL_BUILDING_RE.finditer(bldg_text):
        name = m.group(1)
        if name not in KNOWN_GLOBAL_BUILDINGS:
            continue
        value = int(m.group(2))
        dist = max(1 if value > 0 else 0, round(value * ratio))
        if dist > 0:
            global_buildings[name] = dist

    province_blocks: list[str] = []
    for pm in PROVINCE_BUILDING_RE.finditer(bldg_text):
        province = int(pm.group(1))
        open_idx = bldg_text.find("{", pm.start())
        if open_idx == -1:
            continue
        close_idx = matching_brace(bldg_text, open_idx) + 1
        inner = bldg_text[open_idx + 1 : close_idx - 1].strip()
        if not inner:
            continue
        province_lines = []
        for bm in GLOBAL_BUILDING_RE.finditer(inner):
            bname = bm.group(1)
            bval = int(bm.group(2))
            if bname in KNOWN_PROVINCE_BUILDINGS:
                dist = max(1 if bval > 0 else 0, round(bval * ratio))
                if dist > 0:
                    province_lines.append(f"\t\t\t{bname} = {dist}")
        if province_lines:
            valid = province in valid_provinces
            block_lines = [f"\t\t{province} = {{  # {'OK' if valid else 'BSR_REVIEW province id needs remap'}"]
            block_lines.extend(province_lines)
            block_lines.append("\t\t}")
            province_blocks.append("\n".join(block_lines))
            if not valid:
                issues.append(f"province building {province} not in BSR state {bsr_state_id}, needs province remap")

    if not global_buildings and not province_blocks:
        return None

    lines = ["\tbuildings = {"]
    for name in KNOWN_GLOBAL_BUILDINGS:
        if name in global_buildings:
            lines.append(f"\t\t{name} = {global_buildings[name]}")
    lines.extend(province_blocks)
    lines.append("\t}")
    return "\n".join(lines)


def split_merge_history_for_bsr(tsr: StateFile, bsr: StateFile, mapping_type: str) -> tuple[str, list[str]]:
    issues: list[str] = []
    history = strip_line_comments(tsr.history_block or "")
    owner, controller, cores = history_political_values(tsr)
    overlap = len(tsr.provinces & bsr.provinces)
    tsr_total = max(1, len(tsr.provinces))
    ratio = overlap / tsr_total
    lines = ["history={"]
    if owner:
        lines.append(f"\towner = {owner}")
    if controller:
        lines.append(f"\tcontroller = {controller}")
    for match in VP_RE.finditer(history):
        province = int(match.group(1))
        if province in bsr.provinces:
            lines.append(f"\t{match.group(0)}")
        else:
            issues.append(f"victory_points province {province} not in BSR state {bsr.state_id}")
    buildings_span = find_assignment_span(tsr.history_block or "", "buildings")
    if buildings_span:
        bldg_text = tsr.history_block[buildings_span[0]:buildings_span[1]]
        distributed = distribute_buildings(bldg_text, ratio, bsr.provinces, bsr.state_id, issues)
        if distributed:
            lines.append(distributed)
    for core in sorted(cores):
        lines.append(f"\tadd_core_of = {core}")
    lines.append("}")
    if mapping_type == "merge":
        issues.append("merge owner/controller/cores copied from strongest overlap candidate; review political union manually")
    return "\n".join(lines), issues


def history_political_values(state: StateFile) -> tuple[str, str, set[str]]:
    if not state.history_block:
        return "", "", set()
    history = strip_line_comments(state.history_block)
    owner_match = OWNER_RE.search(history)
    controller_match = CONTROLLER_RE.search(history)
    return (
        owner_match.group(1) if owner_match else "",
        controller_match.group(1) if controller_match else "",
        set(CORE_RE.findall(history)),
    )


def dominant_continent(state: StateFile, definition: dict[int, DefinitionEntry]) -> str:
    counts: dict[str, int] = {}
    for province in state.provinces:
        entry = definition.get(province)
        if not entry:
            continue
        counts[entry.continent] = counts.get(entry.continent, 0) + 1
    if not counts:
        return ""
    continent = max(counts.items(), key=lambda item: item[1])[0]
    return CONTINENT_NAMES.get(continent, continent)


def truth(value: bool) -> str:
    return "yes" if value else "no"


def review_decision_for(row: dict[str, str]) -> tuple[str, str]:
    mapping_type = row["selected_mapping_type"]
    issue_count = int(row["issue_count"])
    alternative_count = int(row["alternative_mapping_count"])
    confidence = float(row["selected_confidence"] or 0)
    has_distribution = (
        row["manual_building_distribution"] == "yes"
        or row["manual_resource_distribution"] == "yes"
    )
    has_conflict = row["owner_core_conflict"] == "yes"
    has_vp_omission = int(row["vp_omission_count"]) > 0

    if mapping_type == "new_bsr_state":
        return "requires_manual", "new BSR state has no TSR overlay candidate"
    if has_conflict:
        return "requires_manual", "owner/controller/core conflict"
    if has_distribution:
        return "requires_manual", "resources/buildings/manpower need manual distribution"
    if has_vp_omission:
        return "requires_manual", "victory point province needs manual placement"
    if issue_count:
        return "requires_manual", "staged merge review issues remain"
    if mapping_type in {"same_id_same_area", "same_name", "province_overlap"} and confidence >= 0.75:
        return "auto_approved", f"{mapping_type} with no review issues"
    if mapping_type == "split" and confidence >= 0.95 and alternative_count <= 1:
        return "auto_approved", "clean one-to-one split target with no review issues"
    return "requires_manual", f"{mapping_type} needs explicit review"


def omit_invalid_province_buildings(history: str, valid_provinces: set[int], bsr_state_id: int, issues: list[str]) -> str:
    output: list[str] = []
    cursor = 0
    for match in PROVINCE_BUILDING_RE.finditer(history):
        province = int(match.group(1))
        if province in valid_provinces:
            continue
        open_index = history.find("{", match.start(), match.end() + 8)
        if open_index == -1:
            continue
        close_index = matching_brace(history, open_index) + 1
        while close_index < len(history) and history[close_index] in " \t":
            close_index += 1
        if close_index < len(history) and history[close_index] == "\n":
            close_index += 1
        output.append(history[cursor : match.start()])
        output.append(f"\t\t# BSR_REVIEW omitted invalid building province {province} for BSR state {bsr_state_id}\n")
        cursor = close_index
        issues.append(f"building province {province} not in BSR state {bsr_state_id}")
    output.append(history[cursor:])
    return "".join(output)


RESOURCE_ITEM_RE = re.compile(r"(\w+)\s*=\s*([0-9.]+)")
MANPOWER_RE = re.compile(r"manpower\s*=\s*([0-9]+)")


def parse_resource_block(block: str) -> dict[str, float]:
    result: dict[str, float] = {}
    for m in RESOURCE_ITEM_RE.finditer(block):
        result[m.group(1)] = float(m.group(2))
    return result


def format_resource_block(resources: dict[str, float], comment: str = "") -> str:
    if not resources:
        return ""
    lines = ["resources={"]
    for name, value in resources.items():
        formatted = f"{value:.3f}" if value != int(value) else str(int(value))
        lines.append(f"\t\t{name} = {formatted}")
    if comment:
        lines[-1] += f"  # {comment}"
    lines.append("\t}")
    return "\n".join(lines)


def distribute_top_blocks(
    tsr: StateFile, bsr: StateFile, mapping_type: str,
) -> tuple[list[str], list[str]]:
    blocks: list[str] = []
    issues: list[str] = []
    overlap = len(tsr.provinces & bsr.provinces)
    tsr_total = max(1, len(tsr.provinces))
    ratio = overlap / tsr_total

    for key in ["state_category", "local_supplies", "impassable"]:
        for block in tsr.top_blocks.get(key, []):
            blocks.append(block)

    for block in tsr.top_blocks.get("manpower", []):
        m = MANPOWER_RE.search(block)
        if m:
            original = int(m.group(1))
            distributed = max(1, round(original * ratio))
            blocks.append(f"manpower={distributed}")
            if distributed != original:
                issues.append(
                    f"manpower distributed: {original} -> {distributed} (ratio={ratio:.3f})"
                )
        else:
            blocks.append(block)

    for block in tsr.top_blocks.get("resources", []):
        parsed = parse_resource_block(block)
        if not parsed:
            continue
        distributed = {}
        for name, value in parsed.items():
            dist = max(0, round(value * ratio))
            if dist > 0:
                distributed[name] = float(dist)
        if distributed:
            blocks.append(
                format_resource_block(
                    distributed,
                    f"proportional from TSR2 state {tsr.state_id} ratio={ratio:.3f}",
                )
            )
        issues.append(
            f"resources distributed from TSR2 state {tsr.state_id} ratio={ratio:.3f}"
        )

    if tsr.state_id != bsr.state_id:
        issues.append(f"TSR state {tsr.state_id} overlaid onto BSR state {bsr.state_id}")
    return blocks, issues


def selected_top_blocks(tsr: StateFile, bsr: StateFile, mapping_type: str = "") -> tuple[list[str], list[str]]:
    if mapping_type in {"split", "merge"}:
        return distribute_top_blocks(tsr, bsr, mapping_type)
    keys = ["manpower", "state_category", "resources", "local_supplies", "impassable"]
    blocks: list[str] = []
    issues: list[str] = []
    for key in keys:
        values = tsr.top_blocks.get(key, [])
        if values:
            blocks.extend(values)
    if tsr.state_id != bsr.state_id:
        issues.append(f"TSR state {tsr.state_id} overlaid onto BSR state {bsr.state_id}")
    return blocks, issues


def render_merged_state(bsr: StateFile, tsr: StateFile | None, mapping_row: dict[str, str] | None) -> tuple[str, list[str]]:
    review_lines: list[str] = []
    lines = [
        "state={",
        f"\tid={bsr.state_id}",
        f'\tname="{bsr.state_name}" # {bsr.display_name}',
    ]
    if mapping_row:
        lines.append(
            f"\t# BSR_MAPPING tsr_state_id={mapping_row['tsr_state_id']} type={mapping_row['mapping_type']} confidence={mapping_row['confidence']}"
        )
    else:
        lines.append("\t# BSR_MAPPING new_bsr_state no_tsr_overlay")

    if tsr:
        mapping_type = mapping_row["mapping_type"] if mapping_row else ""
        blocks, block_issues = selected_top_blocks(tsr, bsr, mapping_type)
        review_lines.extend(block_issues)
        for block in blocks:
            lines.append("")
            lines.extend("\t" + line if line else "" for line in block.splitlines())
        history, history_issues = remap_history_for_bsr(tsr, bsr, mapping_type)
        review_lines.extend(history_issues)
        if history:
            lines.append("")
            lines.extend("\t" + line if line else "" for line in history.splitlines())
    else:
        for key in ["manpower", "state_category", "resources", "local_supplies", "impassable"]:
            for block in bsr.top_blocks.get(key, []):
                lines.append("")
                lines.extend("\t" + line if line else "" for line in block.splitlines())
        if bsr.history_block:
            lines.append("")
            lines.extend("\t" + line if line else "" for line in bsr.history_block.splitlines())
        review_lines.append("new BSR state retained without TSR overlay")

    lines.append("")
    lines.extend("\t" + line if line else "" for line in bsr.province_block.splitlines())
    lines.append("}")
    lines.append("")
    return "\n".join(lines), review_lines


def generate_staged_states(
    repo_root: Path,
    bsr_root: Path,
    mapping_path: Path,
    out_dir: Path,
    manual_decisions_path: Path | None = None,
) -> None:
    tsr_states = parse_states(repo_root / "history" / "states")
    bsr_states = parse_states(bsr_root / "history" / "states")
    bsr_definition = read_definition(bsr_root / "map" / "definition.csv")
    rows = read_mapping(mapping_path)

    def row_overlap(row: dict[str, str]) -> int:
        match = re.search(r"province_overlap=(\d+)", row.get("notes", ""))
        return int(match.group(1)) if match else 0

    def row_score(row: dict[str, str]) -> tuple[float, int, int]:
        confidence = float(row.get("confidence") or 0)
        same_id = 1 if row.get("tsr_state_id") == row.get("bsr_state_id") else 0
        return confidence, row_overlap(row), same_id

    by_bsr: dict[int, dict[str, str]] = {}
    rows_by_bsr: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        if row["bsr_state_id"] and row["mapping_type"] != "new_bsr_state":
            bsr_state_id = int(row["bsr_state_id"])
            rows_by_bsr.setdefault(bsr_state_id, []).append(row)
            if row["mapping_type"] not in AUTOMATIC_MAPPING_TYPES:
                continue
            current = by_bsr.get(bsr_state_id)
            if current is None or row_score(row) > row_score(current):
                by_bsr[bsr_state_id] = row

    applied_manual_decisions: list[dict[str, str]] = []
    invalid_manual_decisions: list[dict[str, str]] = []

    def apply_manual_decisions(path: Path) -> None:
        if not path.exists():
            return
        for decision in read_mapping(path):
            bsr_state_id_text = (decision.get("bsr_state_id") or "").strip()
            action = (decision.get("manual_decision") or "").strip()
            if not bsr_state_id_text or not action:
                continue
            if not bsr_state_id_text.isdigit() or int(bsr_state_id_text) not in bsr_states:
                invalid_manual_decisions.append(
                    {
                        **decision,
                        "issue": "unknown BSR state id",
                    }
                )
                continue
            bsr_state_id = int(bsr_state_id_text)
            current = by_bsr.get(bsr_state_id)
            if action == "approve_selected":
                if not current:
                    invalid_manual_decisions.append(
                        {
                            **decision,
                            "issue": "approve_selected requested but no selected overlay exists",
                        }
                    )
                    continue
                applied_manual_decisions.append(
                    {
                        **decision,
                        "applied_tsr_state_id": current["tsr_state_id"],
                        "applied_mapping_type": current["mapping_type"],
                    }
                )
                continue
            if action == "keep_bsr":
                by_bsr.pop(bsr_state_id, None)
                applied_manual_decisions.append(
                    {
                        **decision,
                        "applied_tsr_state_id": "",
                        "applied_mapping_type": "new_bsr_state",
                    }
                )
                continue
            if action == "override_tsr":
                manual_tsr_state_id = (decision.get("manual_tsr_state_id") or "").strip()
                if not manual_tsr_state_id:
                    invalid_manual_decisions.append(
                        {
                            **decision,
                            "issue": "override_tsr requires manual_tsr_state_id",
                        }
                    )
                    continue
                match = None
                for candidate in rows_by_bsr.get(bsr_state_id, []):
                    if candidate["tsr_state_id"] == manual_tsr_state_id:
                        match = candidate
                        break
                if not match:
                    invalid_manual_decisions.append(
                        {
                            **decision,
                            "issue": "manual_tsr_state_id is not a mapping row for this BSR state",
                        }
                    )
                    continue
                by_bsr[bsr_state_id] = match
                applied_manual_decisions.append(
                    {
                        **decision,
                        "applied_tsr_state_id": match["tsr_state_id"],
                        "applied_mapping_type": match["mapping_type"],
                    }
                )
                continue
            invalid_manual_decisions.append(
                {
                    **decision,
                    "issue": "manual_decision must be approve_selected, keep_bsr, or override_tsr",
                }
            )

    if manual_decisions_path:
        apply_manual_decisions(manual_decisions_path)

    staged_dir = out_dir / "staged_history" / "states"
    if staged_dir.exists():
        shutil.rmtree(staged_dir)
    staged_dir.mkdir(parents=True, exist_ok=True)

    review_rows: list[dict[str, str]] = []
    owner_core_conflicts: list[dict[str, str]] = []
    split_merge_resources: list[dict[str, str]] = []
    europe_russia_priority: list[dict[str, str]] = []
    missing_vp_provinces: list[dict[str, str]] = []
    invalid_building_provinces: list[dict[str, str]] = []
    staged_overlay_decisions: list[dict[str, str]] = []
    for tsr in sorted(tsr_states.values(), key=lambda item: item.state_id):
        if not tsr.history_block:
            continue
        history = strip_line_comments(tsr.history_block)
        for match in VP_RE.finditer(history):
            province = int(match.group(1))
            if province not in bsr_definition:
                missing_vp_provinces.append(
                    {
                        "tsr_state_id": str(tsr.state_id),
                        "tsr_state_name": tsr.display_name,
                        "province": str(province),
                        "issue": "victory point province missing from BSR definition.csv",
                    }
                )
        for match in PROVINCE_BUILDING_RE.finditer(history):
            province = int(match.group(1))
            if province not in bsr_definition:
                invalid_building_provinces.append(
                    {
                        "tsr_state_id": str(tsr.state_id),
                        "tsr_state_name": tsr.display_name,
                        "province": str(province),
                        "issue": "province building reference missing from BSR definition.csv",
                    }
                )
    for row in rows:
        if row["mapping_type"] not in {"split", "merge"} or not row["tsr_state_id"]:
            continue
        tsr = tsr_states.get(int(row["tsr_state_id"]))
        if not tsr or not tsr.top_blocks.get("resources"):
            continue
        split_merge_resources.append(
            {
                "tsr_state_id": row["tsr_state_id"],
                "tsr_state_name": row["tsr_state_name"],
                "bsr_state_id": row["bsr_state_id"],
                "bsr_state_name": row["bsr_state_name"],
                "mapping_type": row["mapping_type"],
                "confidence": row["confidence"],
                "notes": row["notes"],
                "resources": " | ".join(block.replace("\n", " ") for block in tsr.top_blocks["resources"]),
            }
        )
    for row in rows:
        if row["mapping_type"] not in {"manual", "split", "merge", "retired_tsr_state", "new_bsr_state"} and float(row["confidence"] or 0) >= 0.75:
            continue
        tsr = tsr_states.get(int(row["tsr_state_id"])) if row["tsr_state_id"] else None
        bsr = bsr_states.get(int(row["bsr_state_id"])) if row["bsr_state_id"] else None
        tsr_owner, tsr_controller, tsr_cores = history_political_values(tsr) if tsr else ("", "", set())
        bsr_owner, bsr_controller, bsr_cores = history_political_values(bsr) if bsr else ("", "", set())
        political_tags = {tsr_owner, tsr_controller, bsr_owner, bsr_controller} | tsr_cores | bsr_cores
        bsr_continent = dominant_continent(bsr, bsr_definition) if bsr else ""
        is_priority = bsr_continent == "europe" or bool(political_tags & RUSSIA_REVIEW_TAGS)
        if not is_priority:
            continue
        europe_russia_priority.append(
            {
                **{field: row[field] for field in MAPPING_FIELDNAMES},
                "bsr_continent": bsr_continent,
                "tsr_owner": tsr_owner,
                "bsr_owner": bsr_owner,
                "tsr_controller": tsr_controller,
                "bsr_controller": bsr_controller,
                "tsr_cores": " ".join(sorted(tsr_cores)),
                "bsr_cores": " ".join(sorted(bsr_cores)),
            }
        )
    europe_russia_priority.sort(
        key=lambda row: (
            row["mapping_type"] not in {"manual", "merge", "split"},
            -float(row["confidence"] or 0),
            int(row["bsr_state_id"] or 999999),
            int(row["tsr_state_id"] or 999999),
        )
    )
    for bsr in sorted(bsr_states.values(), key=lambda item: item.state_id):
        row = by_bsr.get(bsr.state_id)
        alternatives = rows_by_bsr.get(bsr.state_id, [])
        staged_overlay_decisions.append(
            {
                "bsr_state_id": str(bsr.state_id),
                "bsr_state_name": bsr.display_name,
                "selected_tsr_state_id": row["tsr_state_id"] if row else "",
                "selected_tsr_state_name": row["tsr_state_name"] if row else "",
                "selected_mapping_type": row["mapping_type"] if row else "new_bsr_state",
                "selected_confidence": row["confidence"] if row else "1.000",
                "alternative_mapping_count": str(len(alternatives)),
                "selection_notes": row["notes"] if row else "no TSR overlay candidate",
            }
        )
        tsr = tsr_states.get(int(row["tsr_state_id"])) if row and row["tsr_state_id"] else None
        if tsr:
            tsr_owner, tsr_controller, tsr_cores = history_political_values(tsr)
            bsr_owner, bsr_controller, bsr_cores = history_political_values(bsr)
            if tsr_owner != bsr_owner or tsr_controller != bsr_controller or tsr_cores != bsr_cores:
                owner_core_conflicts.append(
                    {
                        "bsr_state_id": str(bsr.state_id),
                        "bsr_state_name": bsr.display_name,
                        "tsr_state_id": str(tsr.state_id),
                        "tsr_state_name": tsr.display_name,
                        "tsr_owner": tsr_owner,
                        "bsr_owner": bsr_owner,
                        "tsr_controller": tsr_controller,
                        "bsr_controller": bsr_controller,
                        "tsr_cores": " ".join(sorted(tsr_cores)),
                        "bsr_cores": " ".join(sorted(bsr_cores)),
                    }
                )
        text, issues = render_merged_state(bsr, tsr, row)
        write_text(staged_dir / state_filename(bsr), text)
        for issue in issues:
            review_rows.append(
                {
                    "bsr_state_id": str(bsr.state_id),
                    "bsr_state_name": bsr.display_name,
                    "tsr_state_id": row["tsr_state_id"] if row else "",
                    "tsr_state_name": row["tsr_state_name"] if row else "",
                    "issue": issue,
                }
            )

    priority_bsr_ids = {
        int(row["bsr_state_id"])
        for row in europe_russia_priority
        if row["bsr_state_id"]
    }
    review_rows_by_bsr: dict[str, list[dict[str, str]]] = {}
    for row in review_rows:
        review_rows_by_bsr.setdefault(row["bsr_state_id"], []).append(row)
    owner_core_by_bsr = {row["bsr_state_id"]: row for row in owner_core_conflicts}
    resources_by_bsr: dict[str, list[dict[str, str]]] = {}
    for row in split_merge_resources:
        resources_by_bsr.setdefault(row["bsr_state_id"], []).append(row)

    def grouped_decision_row(bsr_state_id: int) -> dict[str, str]:
        bsr = bsr_states[bsr_state_id]
        selected = by_bsr.get(bsr_state_id)
        issues = review_rows_by_bsr.get(str(bsr_state_id), [])
        issue_text = [row["issue"] for row in issues]
        conflict = owner_core_by_bsr.get(str(bsr_state_id))
        resource_rows = resources_by_bsr.get(str(bsr_state_id), [])
        categories = []
        if selected and selected["mapping_type"] in {"split", "merge", "manual"}:
            categories.append(selected["mapping_type"])
        if any(issue.startswith("victory_points province") for issue in issue_text):
            categories.append("vp_review")
        if any(issue.startswith("buildings require manual distribution") for issue in issue_text):
            categories.append("building_distribution")
        if any(issue.startswith("resources require manual distribution") for issue in issue_text) or resource_rows:
            categories.append("resource_distribution")
        if conflict:
            categories.append("owner_core_conflict")
        if not selected:
            categories.append("new_bsr_state")
        decision_row = {
            "bsr_state_id": str(bsr.state_id),
            "bsr_state_name": bsr.display_name,
            "bsr_continent": dominant_continent(bsr, bsr_definition),
            "selected_tsr_state_id": selected["tsr_state_id"] if selected else "",
            "selected_tsr_state_name": selected["tsr_state_name"] if selected else "",
            "selected_mapping_type": selected["mapping_type"] if selected else "new_bsr_state",
            "selected_confidence": selected["confidence"] if selected else "1.000",
            "alternative_mapping_count": str(len(rows_by_bsr.get(bsr_state_id, []))),
            "issue_count": str(len(issues)),
            "vp_omission_count": str(sum(1 for issue in issue_text if issue.startswith("victory_points province"))),
            "manual_building_distribution": truth(any(issue.startswith("buildings require manual distribution") for issue in issue_text)),
            "manual_resource_distribution": truth(any(issue.startswith("resources require manual distribution") for issue in issue_text) or bool(resource_rows)),
            "owner_core_conflict": truth(bool(conflict)),
            "review_categories": " ".join(dict.fromkeys(categories)),
            "selection_notes": selected["notes"] if selected else "no TSR overlay candidate",
        }
        status, reason = review_decision_for(decision_row)
        decision_row["decision_status"] = status
        decision_row["decision_reason"] = reason
        return decision_row

    all_review_decisions = [
        grouped_decision_row(bsr_state_id)
        for bsr_state_id in sorted(bsr_states)
    ]
    grouped_priority = [
        grouped_decision_row(bsr_state_id)
        for bsr_state_id in sorted(priority_bsr_ids)
    ]

    grouped_priority.sort(
        key=lambda row: (
            row["decision_status"] == "auto_approved",
            row["owner_core_conflict"] != "yes",
            row["manual_resource_distribution"] != "yes",
            row["manual_building_distribution"] != "yes",
            -int(row["issue_count"]),
            int(row["bsr_state_id"]),
        )
    )
    all_review_decisions.sort(
        key=lambda row: (
            row["decision_status"] == "auto_approved",
            row["owner_core_conflict"] != "yes",
            row["manual_resource_distribution"] != "yes",
            row["manual_building_distribution"] != "yes",
            -int(row["issue_count"]),
            int(row["bsr_state_id"]),
        )
    )
    write_csv(
        out_dir / "staged_merge_review.csv",
        review_rows,
        ["bsr_state_id", "bsr_state_name", "tsr_state_id", "tsr_state_name", "issue"],
    )
    write_csv(
        out_dir / "staged_overlay_decisions.csv",
        staged_overlay_decisions,
        [
            "bsr_state_id",
            "bsr_state_name",
            "selected_tsr_state_id",
            "selected_tsr_state_name",
            "selected_mapping_type",
            "selected_confidence",
            "alternative_mapping_count",
            "selection_notes",
        ],
    )
    write_csv(
        out_dir / "omitted_victory_points.csv",
        [row for row in review_rows if row["issue"].startswith("victory_points province")],
        ["bsr_state_id", "bsr_state_name", "tsr_state_id", "tsr_state_name", "issue"],
    )
    write_csv(
        out_dir / "omitted_province_buildings.csv",
        [row for row in review_rows if row["issue"].startswith("building province")],
        ["bsr_state_id", "bsr_state_name", "tsr_state_id", "tsr_state_name", "issue"],
    )
    write_csv(
        out_dir / "manual_building_distribution.csv",
        [row for row in review_rows if row["issue"].startswith("buildings require manual distribution")],
        ["bsr_state_id", "bsr_state_name", "tsr_state_id", "tsr_state_name", "issue"],
    )
    write_csv(
        out_dir / "missing_victory_point_provinces.csv",
        missing_vp_provinces,
        ["tsr_state_id", "tsr_state_name", "province", "issue"],
    )
    write_csv(
        out_dir / "invalid_building_provinces.csv",
        invalid_building_provinces,
        ["tsr_state_id", "tsr_state_name", "province", "issue"],
    )
    write_csv(
        out_dir / "owner_core_conflicts.csv",
        owner_core_conflicts,
        [
            "bsr_state_id",
            "bsr_state_name",
            "tsr_state_id",
            "tsr_state_name",
            "tsr_owner",
            "bsr_owner",
            "tsr_controller",
            "bsr_controller",
            "tsr_cores",
            "bsr_cores",
        ],
    )
    write_csv(
        out_dir / "split_merge_resources.csv",
        split_merge_resources,
        [
            "tsr_state_id",
            "tsr_state_name",
            "bsr_state_id",
            "bsr_state_name",
            "mapping_type",
            "confidence",
            "notes",
            "resources",
        ],
    )
    write_csv(
        out_dir / "manual_review_priority_europe_russia.csv",
        europe_russia_priority,
        MAPPING_FIELDNAMES
        + [
            "bsr_continent",
            "tsr_owner",
            "bsr_owner",
            "tsr_controller",
            "bsr_controller",
            "tsr_cores",
            "bsr_cores",
        ],
    )
    write_csv(
        out_dir / "manual_review_priority_europe_russia_grouped.csv",
        grouped_priority,
        REVIEW_DECISION_FIELDNAMES,
    )
    write_csv(
        out_dir / "review_decisions.csv",
        all_review_decisions,
        REVIEW_DECISION_FIELDNAMES,
    )
    write_csv(
        out_dir / "auto_approved_review_decisions.csv",
        [row for row in all_review_decisions if row["decision_status"] == "auto_approved"],
        REVIEW_DECISION_FIELDNAMES,
    )
    write_csv(
        out_dir / "unresolved_review_decisions.csv",
        [row for row in all_review_decisions if row["decision_status"] != "auto_approved"],
        REVIEW_DECISION_FIELDNAMES,
    )
    manual_template_rows = [
        {
            "bsr_state_id": row["bsr_state_id"],
            "bsr_state_name": row["bsr_state_name"],
            "current_selected_tsr_state_id": row["selected_tsr_state_id"],
            "current_selected_tsr_state_name": row["selected_tsr_state_name"],
            "current_mapping_type": row["selected_mapping_type"],
            "suggested_decision_status": row["decision_status"],
            "manual_decision": "",
            "manual_tsr_state_id": "",
            "reviewer_notes": row["decision_reason"],
        }
        for row in all_review_decisions
        if row["decision_status"] != "auto_approved"
    ]
    write_csv(
        out_dir / "manual_decision_template.csv",
        manual_template_rows,
        MANUAL_DECISION_FIELDNAMES,
    )
    write_csv(
        out_dir / "applied_manual_decisions.csv",
        applied_manual_decisions,
        MANUAL_DECISION_FIELDNAMES + ["applied_tsr_state_id", "applied_mapping_type"],
    )
    write_csv(
        out_dir / "invalid_manual_decisions.csv",
        invalid_manual_decisions,
        MANUAL_DECISION_FIELDNAMES + ["issue"],
    )
    write_priority_markdown(out_dir / "manual_review_priority_europe_russia.md", grouped_priority, review_rows_by_bsr, owner_core_by_bsr)


def write_priority_markdown(
    path: Path,
    grouped_priority: list[dict[str, str]],
    review_rows_by_bsr: dict[str, list[dict[str, str]]],
    owner_core_by_bsr: dict[str, dict[str, str]],
    limit: int = 120,
) -> None:
    lines = [
        "# Europe/Russia BSR Manual Review Queue",
        "",
        "Generated by `tools/map_bsr/bsr_map_tool.py all`.",
        "Rows are grouped by BSR state and sorted by conflict/distribution risk.",
        "",
    ]
    for row in grouped_priority[:limit]:
        state_id = row["bsr_state_id"]
        lines.extend(
            [
                f"## BSR {state_id}: {row['bsr_state_name']}",
                "",
                f"- selected TSR: {row['selected_tsr_state_id']} {row['selected_tsr_state_name']}",
                f"- mapping: {row['selected_mapping_type']} confidence={row['selected_confidence']} alternatives={row['alternative_mapping_count']}",
                f"- decision: {row['decision_status']} ({row['decision_reason']})",
                f"- categories: {row['review_categories'] or 'none'}",
                f"- notes: {row['selection_notes']}",
            ]
        )
        conflict = owner_core_by_bsr.get(state_id)
        if conflict:
            lines.extend(
                [
                    f"- owner/controller: TSR {conflict['tsr_owner']}/{conflict['tsr_controller']} vs BSR {conflict['bsr_owner']}/{conflict['bsr_controller']}",
                    f"- cores: TSR `{conflict['tsr_cores']}` vs BSR `{conflict['bsr_cores']}`",
                ]
            )
        issues = review_rows_by_bsr.get(state_id, [])[:8]
        if issues:
            lines.append("- issues:")
            for issue in issues:
                lines.append(f"  - {issue['issue']}")
        lines.append("")
    if len(grouped_priority) > limit:
        lines.append(f"_Showing first {limit} of {len(grouped_priority)} grouped priority states._")
        lines.append("")
    write_text(path, "\n".join(lines))


def validate_state_set(states_dir: Path, definition_path: Path, report_path: Path) -> int:
    definition = read_definition(definition_path)
    land_provinces = {province_id for province_id, entry in definition.items() if entry.is_land and province_id != 0}
    states = parse_states(states_dir)
    errors: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    assigned: dict[int, int] = {}
    for state in states.values():
        if extract_state_ids_from_filename(state.path) != state.state_id:
            warnings.append(
                {
                    "severity": "warning",
                    "state_id": str(state.state_id),
                    "file": str(state.path),
                    "issue": "state id does not match filename prefix",
                }
            )
        for province in sorted(state.provinces):
            if province not in definition:
                errors.append(
                    {
                        "severity": "error",
                        "state_id": str(state.state_id),
                        "file": str(state.path),
                        "issue": f"province {province} missing from definition.csv",
                    }
                )
            elif province in assigned:
                errors.append(
                    {
                        "severity": "error",
                        "state_id": str(state.state_id),
                        "file": str(state.path),
                        "issue": f"province {province} already assigned to state {assigned[province]}",
                    }
                )
            else:
                assigned[province] = state.state_id

        if state.history_block:
            uncommented_history = strip_line_comments(state.history_block)
            for match in VP_RE.finditer(uncommented_history):
                province = int(match.group(1))
                if province not in definition:
                    errors.append(
                        {
                            "severity": "error",
                            "state_id": str(state.state_id),
                            "file": str(state.path),
                            "issue": f"victory point province {province} missing from definition.csv",
                        }
                    )
                elif not definition[province].is_land:
                    errors.append(
                        {
                            "severity": "error",
                            "state_id": str(state.state_id),
                            "file": str(state.path),
                            "issue": f"victory point province {province} is not land",
                        }
                    )
            for match in PROVINCE_BUILDING_RE.finditer(uncommented_history):
                province = int(match.group(1))
                if province not in definition:
                    errors.append(
                        {
                            "severity": "error",
                            "state_id": str(state.state_id),
                            "file": str(state.path),
                            "issue": f"province building {province} missing from definition.csv",
                        }
                    )
                elif not definition[province].is_land:
                    errors.append(
                        {
                            "severity": "error",
                            "state_id": str(state.state_id),
                            "file": str(state.path),
                            "issue": f"province building {province} is not land",
                        }
                    )

    missing_land = sorted(land_provinces - set(assigned))
    for province in missing_land:
        errors.append(
            {
                "severity": "error",
                "state_id": "",
                "file": str(states_dir),
                "issue": f"land province {province} is not assigned to any state",
            }
        )

    rows = errors + warnings
    write_csv(report_path, rows, ["severity", "state_id", "file", "issue"])
    summary = {
        "states": len(states),
        "definition_provinces": len(definition),
        "land_provinces": len(land_provinces),
        "assigned_provinces": len(assigned),
        "errors": len(errors),
        "warnings": len(warnings),
        "report": str(report_path),
    }
    write_text(report_path.with_suffix(".summary.json"), json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return 1 if errors else 0


def validate_network_file(path: Path, definition_path: Path, report_path: Path, mode: str) -> int:
    definition = read_definition(definition_path)
    errors: list[dict[str, str]] = []

    def add_error(file_path: Path, issue: str) -> None:
        errors.append({"severity": "error", "state_id": "", "file": str(file_path), "issue": issue})

    def check_province(file_path: Path, province: int, context: str) -> None:
        if province <= 0:
            return
        if province not in definition:
            add_error(file_path, f"{context}: province {province} missing from definition.csv")

    text = read_text(path) if path.exists() and path.is_file() else ""
    if not path.exists():
        add_error(path, "file missing")
    elif mode == "strategicregions":
        for region_file in sorted(path.glob("*.txt")) if path.is_dir() else [path]:
            region_text = read_text(region_file)
            for span in find_all_assignment_spans(region_text, "provinces"):
                block = region_text[span[0] : span[1]]
                for province in map(int, PROVINCE_TOKEN_RE.findall(block)):
                    check_province(region_file, province, "strategic region")
    elif mode == "adjacency_rules":
        for span_key in ["required_provinces", "icon"]:
            for span in find_all_assignment_spans(text, span_key):
                block = text[span[0] : span[1]]
                for province in map(int, PROVINCE_TOKEN_RE.findall(block)):
                    check_province(path, province, span_key)
    elif mode == "adjacencies":
        with path.open(encoding="utf-8-sig", errors="replace", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            for line_number, row in enumerate(reader, 2):
                for key in ["From", "To", "Through"]:
                    value = (row.get(key) or "").strip()
                    if value and value != "-1":
                        check_province(path, int(value), f"line {line_number} {key}")
    elif mode == "railways":
        for line_number, line in enumerate(text.splitlines(), 1):
            stripped = strip_line_comments(line).strip()
            if not stripped:
                continue
            values = [int(value) for value in re.findall(r"-?\d+", stripped)]
            if len(values) < 3:
                add_error(path, f"line {line_number}: expected level, count, and province path")
                continue
            declared_count = values[1]
            provinces = values[2:]
            if declared_count != len(provinces):
                add_error(path, f"line {line_number}: declared railway province count {declared_count}, found {len(provinces)}")
            for province in provinces:
                check_province(path, province, f"line {line_number} railway")
    elif mode == "supply_nodes":
        for line_number, line in enumerate(text.splitlines(), 1):
            stripped = strip_line_comments(line).strip()
            if not stripped:
                continue
            values = [int(value) for value in re.findall(r"-?\d+", stripped)]
            if len(values) < 2:
                add_error(path, f"line {line_number}: expected supply node level and province")
                continue
            for province in values[1:]:
                check_province(path, province, f"line {line_number} supply node")
    elif mode == "buildings":
        with path.open(encoding="utf-8-sig", errors="replace", newline="") as f:
            for line_number, line in enumerate(f, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                parts = stripped.split(";")
                if len(parts) < 7:
                    add_error(path, f"line {line_number}: expected 7 semicolon fields")
                    continue
                province = int(float(parts[6]))
                check_province(path, province, f"line {line_number} building linked province")
    elif mode == "unitstacks":
        with path.open(encoding="utf-8-sig", errors="replace", newline="") as f:
            for line_number, line in enumerate(f, 1):
                stripped = line.strip()
                if not stripped or stripped.startswith("#"):
                    continue
                parts = stripped.split(";")
                if not parts:
                    continue
                province = int(float(parts[0]))
                check_province(path, province, f"line {line_number} unitstack")
    else:
        for line_number, line in enumerate(text.splitlines(), 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            for province in map(int, re.findall(r"\b\d+\b", stripped)):
                check_province(path, province, f"line {line_number}")
    write_csv(report_path, errors, ["severity", "state_id", "file", "issue"])
    return 1 if errors else 0


def command_snapshot(args: argparse.Namespace) -> int:
    snapshot(args.repo_root, args.bsr_root, args.out_dir)
    return 0


def command_map(args: argparse.Namespace) -> int:
    tsr_states = parse_states(args.repo_root / "history" / "states")
    bsr_states = parse_states(args.bsr_root / "history" / "states")
    rows = build_mapping(tsr_states, bsr_states)
    write_csv(args.out_dir / "state_mapping.csv", rows, MAPPING_FIELDNAMES)
    collect_mapping_reports(rows, args.out_dir)
    return 0


def command_generate(args: argparse.Namespace) -> int:
    generate_staged_states(args.repo_root, args.bsr_root, args.mapping, args.out_dir, args.decisions)
    return 0


def command_validate(args: argparse.Namespace) -> int:
    return validate_state_set(args.states_dir, args.definition, args.report)


def command_validate_network(args: argparse.Namespace) -> int:
    return validate_network_file(args.path, args.definition, args.report, args.mode)


def command_all(args: argparse.Namespace) -> int:
    snapshot(args.repo_root, args.bsr_root, args.out_dir)
    map_args = argparse.Namespace(repo_root=args.repo_root, bsr_root=args.bsr_root, out_dir=args.out_dir)
    command_map(map_args)
    mapping = args.out_dir / "state_mapping.csv"
    generate_staged_states(args.repo_root, args.bsr_root, mapping, args.out_dir, args.decisions)
    exit_code = validate_state_set(
        args.out_dir / "staged_history" / "states",
        args.bsr_root / "map" / "definition.csv",
        args.out_dir / "staged_state_validation.csv",
    )
    network_checks = [
        (
            args.bsr_root / "map" / "strategicregions",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "bsr_strategicregions_validation.csv",
            "strategicregions",
        ),
        (
            args.bsr_root / "map" / "adjacencies.csv",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "bsr_adjacencies_validation.csv",
            "adjacencies",
        ),
        (
            args.bsr_root / "map" / "adjacency_rules.txt",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "bsr_adjacency_rules_validation.csv",
            "adjacency_rules",
        ),
        (
            args.bsr_root / "map" / "buildings.txt",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "bsr_buildings_validation.csv",
            "buildings",
        ),
        (
            args.bsr_root / "map" / "unitstacks.txt",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "bsr_unitstacks_validation.csv",
            "unitstacks",
        ),
        (
            args.repo_root / "map" / "railways.txt",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "tsr_railways_vs_bsr_definition_validation.csv",
            "railways",
        ),
        (
            args.repo_root / "map" / "supply_nodes.txt",
            args.bsr_root / "map" / "definition.csv",
            args.out_dir / "tsr_supply_nodes_vs_bsr_definition_validation.csv",
            "supply_nodes",
        ),
    ]
    for path, definition, report, mode in network_checks:
        exit_code |= validate_network_file(path, definition, report, mode)
    return exit_code


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--bsr-root", type=Path, default=DEFAULT_BSR_ROOT)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    subparsers = parser.add_subparsers(required=True)

    snapshot_parser = subparsers.add_parser("snapshot")
    snapshot_parser.set_defaults(func=command_snapshot)

    map_parser = subparsers.add_parser("map")
    map_parser.set_defaults(func=command_map)

    generate_parser = subparsers.add_parser("generate")
    generate_parser.add_argument("--mapping", type=Path, default=DEFAULT_OUT_DIR / "state_mapping.csv")
    generate_parser.add_argument("--decisions", type=Path, default=DEFAULT_MANUAL_DECISIONS)
    generate_parser.set_defaults(func=command_generate)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("--states-dir", type=Path, required=True)
    validate_parser.add_argument("--definition", type=Path, required=True)
    validate_parser.add_argument("--report", type=Path, required=True)
    validate_parser.set_defaults(func=command_validate)

    network_parser = subparsers.add_parser("validate-network")
    network_parser.add_argument("--path", type=Path, required=True)
    network_parser.add_argument("--definition", type=Path, required=True)
    network_parser.add_argument("--report", type=Path, required=True)
    network_parser.add_argument(
        "--mode",
        choices=[
            "strategicregions",
            "adjacency_rules",
            "adjacencies",
            "railways",
            "supply_nodes",
            "buildings",
            "unitstacks",
            "flat",
        ],
        default="flat",
    )
    network_parser.set_defaults(func=command_validate_network)

    all_parser = subparsers.add_parser("all")
    all_parser.add_argument("--decisions", type=Path, default=DEFAULT_MANUAL_DECISIONS)
    all_parser.set_defaults(func=command_all)
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.repo_root = args.repo_root.resolve()
    args.bsr_root = args.bsr_root.resolve()
    args.out_dir = args.out_dir.resolve()
    if hasattr(args, "mapping"):
        args.mapping = args.mapping.resolve()
    if hasattr(args, "decisions"):
        args.decisions = args.decisions.resolve()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
