#!/usr/bin/env python3
"""Auto-generate railways and supply nodes for BSR map.

Algorithm:
  1. Build province adjacency graph from provinces.bmp
  2. Extract VP locations from BSR state files (hub positions)
  3. Build railway network connecting hubs via shortest land paths
  4. Generate supply nodes at VP locations
"""

from __future__ import annotations

import heapq
import json
import re
import sys
from collections import defaultdict
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
    strip_line_comments,
    write_text,
)

VP_VALUE_RE = re.compile(r"(\d+)\s+([-+]?\d+(?:\.\d+)?)")

BSR_ROOT = DEFAULT_BSR_ROOT
GENERATED_DIR = Path("tools/map_bsr/generated")


def build_province_centers_and_adjacency(
    bmp_path: Path, definition: dict[int, DefinitionEntry]
) -> tuple[dict[int, tuple[float, float]], dict[int, set[int]]]:
    from PIL import Image

    img = Image.open(bmp_path)
    if img.mode != "RGB":
        img = img.convert("RGB")
    width, height = img.size
    pixels = img.load()

    color_to_id: dict[tuple[int, int, int], int] = {}
    for entry in definition.values():
        parts = entry.raw.split(";")
        if len(parts) >= 4:
            r, g, b = int(parts[1]), int(parts[2]), int(parts[3])
            color_to_id[(r, g, b)] = entry.province_id

    land_provinces = {pid for pid, e in definition.items() if e.is_land}

    sums: dict[int, list[float]] = {}
    counts: dict[int, int] = {}
    adjacency: dict[int, set[int]] = defaultdict(set)

    prev_row: dict[int, int] = {}
    curr_row: dict[int, int] = {}

    for y in range(height):
        curr_row.clear()
        for x in range(width):
            r, g, b = pixels[x, y]
            pid = color_to_id.get((r, g, b))
            if pid is None or pid not in land_provinces:
                continue

            s = sums.setdefault(pid, [0.0, 0.0])
            s[0] += x
            s[1] += y
            counts[pid] = counts.get(pid, 0) + 1

            curr_row[x] = pid

            # Horizontal adjacency (left neighbor)
            if x > 0 and (x - 1) in curr_row:
                other = curr_row[x - 1]
                if other != pid:
                    adjacency[pid].add(other)
                    adjacency[other].add(pid)

            # Vertical adjacency (pixel above)
            if y > 0 and x in prev_row:
                other = prev_row[x]
                if other != pid:
                    adjacency[pid].add(other)
                    adjacency[other].add(pid)

        prev_row, curr_row = curr_row, prev_row

    centers: dict[int, tuple[float, float]] = {}
    for pid, s in sums.items():
        c = counts[pid]
        centers[pid] = (s[0] / c, s[1] / c)

    return centers, dict(adjacency)


def extract_bsr_vps(bsr_states_dir: Path, definition: dict[int, DefinitionEntry]) -> dict[int, list[tuple[int, int]]]:
    """Extract VP data: state_id -> [(province, value)]."""
    states = parse_states(bsr_states_dir)
    result: dict[int, list[tuple[int, int]]] = {}
    VP_FULL = re.compile(r"victory_points\s*=\s*\{([^}]*)\}", re.DOTALL)
    VP_VAL = re.compile(r"(\d+)\s+([-+]?\d+(?:\.\d+)?)")
    for state in states.values():
        if not state.history_block:
            continue
        hist = strip_line_comments(state.history_block)
        vps: list[tuple[int, int]] = []
        for m in VP_FULL.finditer(hist):
            for vm in VP_VAL.finditer(m.group(1)):
                prov = int(vm.group(1))
                val = int(float(vm.group(2)))
                if prov in definition:
                    vps.append((prov, val))
        if vps:
            result[state.state_id] = vps
    return result


def distance_sq(a: tuple[float, float], b: tuple[float, float]) -> float:
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def dijkstra(
    start: int,
    adjacency: dict[int, set[int]],
    centers: dict[int, tuple[float, float]],
    targets: set[int],
    max_dist_sq: float = float("inf"),
) -> dict[int, list[int]]:
    if start not in adjacency:
        return {}
    dist: dict[int, float] = {start: 0.0}
    prev: dict[int, int] = {}
    pq: list[tuple[float, int]] = [(0.0, start)]
    found: dict[int, list[int]] = {}

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        if u in targets and u != start:
            path = []
            node = u
            while node in prev:
                path.append(node)
                node = prev[node]
            path.append(start)
            path.reverse()
            found[u] = path
            if len(found) == len(targets):
                break
        for v in adjacency.get(u, set()):
            if v not in centers:
                continue
            edge_dist = distance_sq(centers[u], centers[v])
            new_dist = d + edge_dist
            if new_dist < dist.get(v, float("inf")):
                if new_dist > max_dist_sq:
                    continue
                dist[v] = new_dist
                prev[v] = u
                heapq.heappush(pq, (new_dist, v))

    return found


def generate_railways(
    vps_by_state: dict[int, list[tuple[int, int]]],
    centers: dict[int, tuple[float, float]],
    adjacency: dict[int, set[int]],
    bsr_root: Path,
) -> list[str]:
    """Generate railway lines connecting VPs."""
    # Collect all VP provinces with their values
    all_vps: dict[int, int] = {}
    for state_id, vp_list in vps_by_state.items():
        for prov, val in vp_list:
            all_vps[prov] = max(all_vps.get(prov, 0), val)

    if not all_vps:
        return []

    # Sort VPs by value (descending) for priority
    vp_sorted = sorted(all_vps.items(), key=lambda x: -x[1])
    vp_provinces = set(all_vps.keys())

    # Build connections: MST-like approach connecting nearby VPs
    connected: set[int] = set()
    connections: list[tuple[int, int, float]] = []  # (from, to, dist_sq)

    if vp_sorted:
        # Start with highest-value VP
        seed = vp_sorted[0][0]
        connected.add(seed)

        # Greedy nearest-neighbor MST
        remaining = vp_provinces - connected
        while remaining:
            best_dist = float("inf")
            best_from = -1
            best_to = -1
            for c in connected:
                if c not in centers:
                    continue
                for r in remaining:
                    if r not in centers:
                        continue
                    d = distance_sq(centers[c], centers[r])
                    if d < best_dist:
                        best_dist = d
                        best_from = c
                        best_to = r

            if best_to == -1:
                break
            connected.add(best_to)
            remaining.discard(best_to)
            connections.append((best_from, best_to, best_dist))

    # For very distant connections, skip (would create unrealistic long railways)
    max_connection_dist = (max(p[0] for p in centers.values()) if centers else 1000) * 0.15
    max_connection_dist_sq = max_connection_dist ** 2

    # Find paths through adjacency graph
    railway_lines: list[str] = []
    path_cache: dict[frozenset, list[int]] = {}

    for from_prov, to_prov, dist_sq in connections:
        if dist_sq > max_connection_dist_sq * 4:
            continue

        key = frozenset({from_prov, to_prov})
        if key in path_cache:
            path = path_cache[key]
        else:
            paths = dijkstra(from_prov, adjacency, centers, {to_prov}, max_connection_dist_sq * 2)
            path = paths.get(to_prov)
            if path is None:
                continue
            path_cache[key] = path

        if len(path) < 2:
            continue

        # Determine railway level based on VP values
        min_vp_val = min(all_vps.get(from_prov, 0), all_vps.get(to_prov, 0))
        max_vp_val = max(all_vps.get(from_prov, 0), all_vps.get(to_prov, 0))

        if max_vp_val >= 20:
            level = 3
        elif max_vp_val >= 5:
            level = 2
        else:
            level = 1

        count = len(path)
        prov_str = " ".join(str(p) for p in path)
        railway_lines.append(f"{level} {count} {prov_str}")

    return railway_lines


def generate_supply_nodes(
    vps_by_state: dict[int, list[tuple[int, int]]],
) -> list[str]:
    """Generate supply nodes at VP locations."""
    all_vps: dict[int, int] = {}
    for vp_list in vps_by_state.values():
        for prov, val in vp_list:
            all_vps[prov] = max(all_vps.get(prov, 0), val)

    lines: list[str] = []
    for prov in sorted(all_vps.keys()):
        val = all_vps[prov]
        if val >= 20:
            level = 3
        elif val >= 5:
            level = 2
        else:
            level = 1
        lines.append(f"{level} {prov}")

    return lines


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bsr-root", type=Path, default=BSR_ROOT)
    parser.add_argument("--out-dir", type=Path, default=GENERATED_DIR)
    args = parser.parse_args()

    bsr_root = args.bsr_root.resolve()
    out_dir = args.out_dir.resolve()

    print("Reading BSR definition.csv...")
    definition = read_definition(bsr_root / "map" / "definition.csv")

    print("Building province adjacency from provinces.bmp (this takes a while)...")
    centers, adjacency = build_province_centers_and_adjacency(bsr_root / "map" / "provinces.bmp", definition)
    print(f"  {len(centers)} province centers, {len(adjacency)} adjacency entries")

    # Stats
    total_edges = sum(len(v) for v in adjacency.values()) // 2
    print(f"  {total_edges} adjacency edges")

    print("Extracting BSR VPs...")
    vps_by_state = extract_bsr_vps(bsr_root / "history" / "states", definition)
    total_vps = sum(len(v) for v in vps_by_state.values())
    print(f"  {len(vps_by_state)} states with VPs, {total_vps} VP entries")

    print("Generating supply nodes...")
    supply_lines = generate_supply_nodes(vps_by_state)
    print(f"  {len(supply_lines)} supply nodes")

    print("Generating railway network...")
    railway_lines = generate_railways(vps_by_state, centers, adjacency, bsr_root)
    print(f"  {len(railway_lines)} railway lines")

    # Write outputs
    rail_path = out_dir / "generated_railways.txt"
    write_text(rail_path, "\n".join(railway_lines) + "\n")
    print(f"Railways written to {rail_path}")

    supply_path = out_dir / "generated_supply_nodes.txt"
    write_text(supply_path, "\n".join(supply_lines) + "\n")
    print(f"Supply nodes written to {supply_path}")

    summary = {
        "province_centers": len(centers),
        "adjacency_edges": total_edges,
        "states_with_vps": len(vps_by_state),
        "total_vps": total_vps,
        "railway_lines": len(railway_lines),
        "supply_nodes": len(supply_lines),
    }
    write_text(out_dir / "railway_generation_summary.json", json.dumps(summary, indent=2) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
