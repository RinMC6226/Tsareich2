#!/usr/bin/env python3
"""Parliament diagram generator for Tsareich2 HOI4 mod.

Generates (decisions panel only — no politics-tab window):
  interface/{TAG}_parliament.gfx             -- sprite definitions
  interface/{TAG}_parliament_decisions.gui   -- decisions panel window
  common/scripted_guis/{TAG}_parliament_sg.txt  -- decision_category scripted_gui
  gfx/interface/parliament/{TAG}_parliament_seat_{party}.tga  -- per-party seat icons
  gfx/interface/parliament/{TAG}_parliament_gov_marker.tga    -- governing marker icon

Also patches:
  interface/countrypoliticsview.gui  -- removes clipping=no added by older generator versions

Usage:
  python generate_parliament.py [path/to/config.yml]
  Default config: parliaments/GER_default.yml
"""

import math
import sys
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

try:
    from PIL import Image, ImageDraw
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    from parliamentarch import get_row_thickness, get_seats_centers
    from parliamentarch.geometry import FillingStrategy
    HAS_PARLIAMENTARCH = True
except ImportError:
    HAS_PARLIAMENTARCH = False

# ─── Seat placement ──────────────────────────────────────────────────────────

def compute_seat_positions_legacy(total_seats, rows, cx, cy, r_inner, r_outer, seat_order="angle", radial_order="inner_to_outer"):
    if rows <= 0:
        raise ValueError("rows must be positive")

    if rows == 1:
        radii = [r_inner]
    else:
        radii = [r_inner + (r_outer - r_inner) * i / (rows - 1) for i in range(rows)]
    total_r = sum(radii)
    seats_per_row = [round(total_seats * r / total_r) for r in radii]
    diff = total_seats - sum(seats_per_row)
    fracs = sorted(
        range(rows),
        key=lambda i: (total_seats * radii[i] / total_r) - seats_per_row[i],
        reverse=(diff > 0),
    )
    for i in range(abs(diff)):
        seats_per_row[fracs[i]] += 1 if diff > 0 else -1
    positions = []
    for r, n in zip(radii, seats_per_row):
        for j in range(n):
            theta = math.pi - (math.pi * j / (n - 1)) if n > 1 else math.pi / 2
            x = cx + r * math.cos(theta)
            y = cy - r * math.sin(theta)
            positions.append((round(x), round(y), theta, r))

    # Match parliamentdiagram-style wedges more closely by assigning seats
    # primarily along the angular sweep, then deciding whether the same angle
    # fills from the inner row or the outer row first.
    if seat_order == "angle":
        radius_key = (lambda p: p[3]) if radial_order == "inner_to_outer" else (lambda p: -p[3])
        positions.sort(key=lambda p: (-p[2], radius_key(p), p[0], p[1]))
    elif seat_order == "legacy_x":
        positions.sort(key=lambda p: (p[0], -p[1], p[3]))
    else:
        raise ValueError(f"Unsupported seat_order: {seat_order}")

    positions = [(x, y) for x, y, _theta, _radius in positions]
    assert len(positions) == total_seats
    return positions


def compute_seat_positions_parliamentarch(total_seats, rows, cx, cy, r_outer,
                                          seat_order="angle", filling_strategy="default", span_angle=180):
    if not HAS_PARLIAMENTARCH:
        raise RuntimeError("parliamentarch is not installed")

    strategy_map = {
        "default": FillingStrategy.DEFAULT,
        "empty_inner": FillingStrategy.EMPTY_INNER,
        "outer_priority": FillingStrategy.OUTER_PRIORITY,
    }
    if filling_strategy not in strategy_map:
        raise ValueError(f"Unsupported filling_strategy: {filling_strategy}")

    centers = get_seats_centers(
        total_seats,
        min_nrows=rows,
        filling_strategy=strategy_map[filling_strategy],
        span_angle=span_angle,
    )

    if seat_order == "angle":
        ordered = sorted(centers.items(), key=lambda item: item[1], reverse=True)
    elif seat_order == "angle_reverse":
        ordered = sorted(centers.items(), key=lambda item: item[1])
    else:
        raise ValueError(f"Unsupported seat_order for parliamentarch: {seat_order}")

    positions = []
    for (px, py), _angle in ordered:
        x = cx + (px - 1.0) * r_outer
        y = cy - py * r_outer
        positions.append((round(x), round(y)))

    assert len(positions) == total_seats
    return positions


def compute_seat_positions(total_seats, rows, cx, cy, r_inner, r_outer,
                           seat_order="angle", radial_order="inner_to_outer",
                           layout_engine="auto", filling_strategy="default", span_angle=180):
    if layout_engine in ("auto", "parliamentarch") and HAS_PARLIAMENTARCH:
        return compute_seat_positions_parliamentarch(
            total_seats,
            rows,
            cx,
            cy,
            r_outer,
            seat_order=seat_order,
            filling_strategy=filling_strategy,
            span_angle=span_angle,
        )

    return compute_seat_positions_legacy(
        total_seats,
        rows,
        cx,
        cy,
        r_inner,
        r_outer,
        seat_order=seat_order,
        radial_order=radial_order,
    )


def compute_auto_seat_size(rows, r_outer, seat_radius_factor=0.62, layout_engine="auto"):
    if layout_engine in ("auto", "parliamentarch") and HAS_PARLIAMENTARCH:
        diameter = 2 * seat_radius_factor * get_row_thickness(rows) * r_outer
        return max(4, round(diameter))

    return max(4, round(r_outer / max(rows * 3.5, 1)))

# ─── GFX ─────────────────────────────────────────────────────────────────────

def generate_gfx(parties, tag):
    prefix = f"GER_parliament" if tag == "GER" else f"{tag}_parliament"
    lines = ["spriteTypes = {"]
    for p in parties:
        pid = p["id"]
        lines += [
            "\tspriteType = {",
            f'\t\tname = "GFX_{prefix}_seat_{pid}"',
            f'\t\ttexturefile = "gfx/interface/parliament/{prefix}_seat_{pid}.tga"',
            "\t\tnoOfFrames = 1",
            "\t}",
        ]
    lines += [
        "\tspriteType = {",
        f'\t\tname = "GFX_{prefix}_gov_marker"',
        f'\t\ttexturefile = "gfx/interface/parliament/{prefix}_gov_marker.tga"',
        "\t\tnoOfFrames = 1",
        "\t}",
    ]
    lines.append("}")
    return "\n".join(lines) + "\n"

# ─── GUI helpers ─────────────────────────────────────────────────────────────

def _icon_lines(seat, party_id, x, y, half, name_prefix, gfx_prefix, indent):
    return [
        f"{indent}iconType = {{",
        f'{indent}\tname = "{name_prefix}_{seat:03d}_{party_id}"',
        f'{indent}\tspriteType = "GFX_{gfx_prefix}_seat_{party_id}"',
        f"{indent}\tposition = {{ x = {x - half} y = {y - half} }}",
        f"{indent}}}",
    ]

# ─── GUI (decisions panel) ────────────────────────────────────────────────────

def generate_decisions_gui(positions, parties, width, height, seat_size, cx, cy, tag):
    half = seat_size // 2
    prefix = f"{tag}_parliament"
    gfx_prefix = f"{tag}_parliament" if tag == "GER" else f"{tag}_parliament"

    min_seat_x = min(x for x, y in positions) - half
    max_seat_x = max(x for x, y in positions) + half
    seat_block_w = max_seat_x - min_seat_x
    legend_gap = 18
    legend_block_w = 340
    content_left = max(10, round((width - (seat_block_w + legend_gap + legend_block_w)) / 2))
    shift_x = content_left - min_seat_x
    positions = [(x + shift_x, y) for x, y in positions]
    cx += shift_x
    legend_x = content_left + seat_block_w + legend_gap

    gov_marker_size = 8
    legend_spacing = 18
    summary_y_start = 24
    legend_y_start = 64
    label_x = legend_x + seat_size + 4
    stats_x = legend_x + 190
    stats_w = max(75, legend_block_w - (stats_x - legend_x) - gov_marker_size - 8)
    label_w = max(55, stats_x - label_x - 8)

    title_loc = f"{tag}_PARLIAMENT_TITLE"
    content_w = seat_block_w + legend_gap + legend_block_w

    lines = [
        "guiTypes = {",
        "\tcontainerWindowType = {",
        f'\t\tname = "{prefix}_decisions_window"',
        f"\t\tsize = {{ width = {width} height = {height} }}",
        "\t\tclipping = no",
        "",
        "\t\tinstantTextboxType = {",
        f'\t\t\tname = "{prefix}_decisions_title"',
        f"\t\t\tposition = {{ x = {content_left} y = 4 }}",
        '\t\t\tfont = "hoi_18mbs"',
        f'\t\t\ttext = "{title_loc}"',
        "\t\t\tformat = center",
        f"\t\t\tmaxWidth = {content_w}",
        "\t\t\tmaxHeight = 20",
        "\t\t\tfixedsize = yes",
        "\t\t}",
        "",
        "\t\t# Total seats label at bottom center of diagram",
        "\t\tinstantTextboxType = {",
        f'\t\t\tname = "{prefix}_total_seats_label"',
        f"\t\t\tposition = {{ x = {cx - 25} y = {cy + 5} }}",
        '\t\t\tfont = "hoi_14b"',
        f'\t\t\ttext = "{tag}_PARL_TOTAL_SEATS"',
        "\t\t\tmaxWidth = 50",
        "\t\t\tmaxHeight = 14",
        "\t\t\tfixedsize = yes",
        "\t\t}",
        "",
        "\t\tinstantTextboxType = {",
        f'\t\t\tname = "{prefix}_government_total"',
        f"\t\t\tposition = {{ x = {legend_x} y = {summary_y_start} }}",
        '\t\t\tfont = "hoi_14b"',
        f'\t\t\ttext = "{tag}_PARL_GOVERNMENT_TOTAL"',
        "\t\t\tformat = left",
        f"\t\t\tmaxWidth = {legend_block_w}",
        "\t\t\tmaxHeight = 14",
        "\t\t\tfixedsize = yes",
        "\t\t}",
        "",
        "\t\tinstantTextboxType = {",
        f'\t\t\tname = "{prefix}_opposition_total"',
        f"\t\t\tposition = {{ x = {legend_x} y = {summary_y_start + 18} }}",
        '\t\t\tfont = "hoi_14b"',
        f'\t\t\ttext = "{tag}_PARL_OPPOSITION_TOTAL"',
        "\t\t\tformat = left",
        f"\t\t\tmaxWidth = {legend_block_w}",
        "\t\t\tmaxHeight = 14",
        "\t\t\tfixedsize = yes",
        "\t\t}",
        "",
    ]

    for i, (x, y) in enumerate(positions):
        seat = i + 1
        for p in parties:
            lines += _icon_lines(seat, p["id"], x, y, half,
                                  f"{prefix}_dseat", gfx_prefix, "\t\t")

    # Right column: legend with party name + governing marker
    lines.append("")
    for idx, p in enumerate(parties):
        pid = p["id"]
        ly = legend_y_start + idx * legend_spacing
        name_loc_key = f"{tag}_PARL_NAME_{pid.upper()}"
        stats_loc_key = f"{tag}_PARL_STATS_{pid.upper()}"

        lines += [
            "\t\ticonType = {",
            f'\t\t\tname = "{prefix}_legend_{pid}_icon"',
            f'\t\t\tspriteType = "GFX_{gfx_prefix}_seat_{pid}"',
            f"\t\t\tposition = {{ x = {legend_x} y = {ly} }}",
            "\t\t}",
            "\t\tinstantTextboxType = {",
            f'\t\t\tname = "{prefix}_legend_{pid}_label"',
            f"\t\t\tposition = {{ x = {label_x} y = {ly + 1} }}",
            '\t\t\tfont = "hoi_14b"',
            f'\t\t\ttext = "{name_loc_key}"',
            "\t\t\tformat = left",
            f"\t\t\tmaxWidth = {label_w}",
            "\t\t\tmaxHeight = 14",
            "\t\t\tfixedsize = yes",
            "\t\t}",
            "\t\tinstantTextboxType = {",
            f'\t\t\tname = "{prefix}_legend_{pid}_stats"',
            f"\t\t\tposition = {{ x = {stats_x} y = {ly + 1} }}",
            '\t\t\tfont = "hoi_12b"',
            f'\t\t\ttext = "{stats_loc_key}"',
            "\t\t\tformat = right",
            f"\t\t\tmaxWidth = {stats_w}",
            "\t\t\tmaxHeight = 14",
            "\t\t\tfixedsize = yes",
            "\t\t}",
            "\t\ticonType = {",
            f'\t\t\tname = "{prefix}_legend_{pid}_gov_marker"',
            f'\t\t\tspriteType = "GFX_{gfx_prefix}_gov_marker"',
            f"\t\t\tposition = {{ x = {legend_x + legend_block_w - gov_marker_size - 2} y = {ly} }}",
            "\t\t}",
        ]

    lines += ["\t}", "}"]
    return "\n".join(lines) + "\n"

# ─── Revert countrypoliticsview.gui ──────────────────────────────────────────

def revert_countrypoliticsview(mod_root):
    """Remove clipping=no added by older generator versions."""
    path = mod_root / "interface" / "countrypoliticsview.gui"
    if not path.exists():
        print("  [INFO] countrypoliticsview.gui not found, skipping")
        return

    content = path.read_text(encoding="utf-8")
    changed = False

    size_token = 'size = { width=550 height=100%% }'
    clip_suffix = '\n\t\tclipping = no'
    if size_token + clip_suffix in content:
        content = content.replace(size_token + clip_suffix, size_token)
        print("  [revert] Removed clipping=no from countrypoliticsview.gui")
        changed = True

    if changed:
        path.write_text(content, encoding="utf-8")
    else:
        print("  [revert] countrypoliticsview.gui already clean")

# ─── Scripted GUI ─────────────────────────────────────────────────────────────

def _seat_trigger_lines(total_seats, parties, seat_prefix, var_prefix):
    """Generate visibility triggers for seat icons: each seat shows the correct party color."""
    lines = []
    party_ids = [p["id"] for p in parties]
    for seat in range(1, total_seats + 1):
        for idx, pid in enumerate(party_ids):
            max_var = f"{var_prefix}_{pid}_max"
            tname = f"{seat_prefix}_{seat:03d}_{pid}_visible"
            if idx == 0:
                lines += [
                    f"\t\t\t{tname} = {{",
                    f"\t\t\t\tcheck_variable = {{",
                    f"\t\t\t\t\tvar = {max_var}",
                    f"\t\t\t\t\tvalue = {seat}",
                    f"\t\t\t\t\tcompare = greater_than_or_equals",
                    f"\t\t\t\t}}",
                    "\t\t\t}",
                ]
            elif idx == len(party_ids) - 1:
                prev_max = f"{var_prefix}_{party_ids[idx-1]}_max"
                lines += [
                    f"\t\t\t{tname} = {{",
                    f"\t\t\t\tNOT = {{",
                    f"\t\t\t\t\tcheck_variable = {{",
                    f"\t\t\t\t\t\tvar = {prev_max}",
                    f"\t\t\t\t\t\tvalue = {seat}",
                    f"\t\t\t\t\t\tcompare = greater_than_or_equals",
                    f"\t\t\t\t\t}}",
                    f"\t\t\t\t}}",
                    "\t\t\t}",
                ]
            else:
                prev_max = f"{var_prefix}_{party_ids[idx-1]}_max"
                lines += [
                    f"\t\t\t{tname} = {{",
                    f"\t\t\t\tNOT = {{",
                    f"\t\t\t\t\tcheck_variable = {{",
                    f"\t\t\t\t\t\tvar = {prev_max}",
                    f"\t\t\t\t\t\tvalue = {seat}",
                    f"\t\t\t\t\t\tcompare = greater_than_or_equals",
                    f"\t\t\t\t\t}}",
                    f"\t\t\t\t}}",
                    f"\t\t\t\tcheck_variable = {{",
                    f"\t\t\t\t\tvar = {max_var}",
                    f"\t\t\t\t\tvalue = {seat}",
                    f"\t\t\t\t\tcompare = greater_than_or_equals",
                    f"\t\t\t\t}}",
                    "\t\t\t}",
                ]
    return lines


def _gov_marker_trigger_lines(parties, prefix, var_prefix):
    """Generate visibility triggers for governing marker icons in legend."""
    lines = []
    for p in parties:
        pid = p["id"]
        gov_flag = f"{var_prefix}_{pid}_is_governing"
        tname = f"{prefix}_legend_{pid}_gov_marker_visible"
        lines += [
            f"\t\t\t{tname} = {{",
            f"\t\t\t\thas_country_flag = {gov_flag}",
            "\t\t\t}",
        ]
    return lines


def generate_sg(total_seats, parties, tag):
    prefix = f"{tag}_parliament"
    var_prefix = f"{tag}_parliament"
    window_name = f"{prefix}_decisions_window"
    dirty_var = f"{prefix}_dirty"

    lines = ["scripted_gui = {"]
    lines += [
        f"\t{prefix}_decisions_gui = {{",
        "\t\tcontext_type = decision_category",
        f'\t\twindow_name = "{window_name}"',
        "",
        f"\t\tdirty = {dirty_var}",
        "",
        "\t\ttriggers = {",
    ]
    lines += _seat_trigger_lines(total_seats, parties, f"{prefix}_dseat", var_prefix)
    lines += _gov_marker_trigger_lines(parties, prefix, var_prefix)
    lines += ["\t\t}", "\t}", "}"]
    return "\n".join(lines) + "\n"

# ─── TGA seat icons ───────────────────────────────────────────────────────────

def generate_seat_icons(parties, seat_size, out_dir, prefix):
    if not HAS_PIL:
        print("[WARN] Pillow not found. Skipping TGA generation. Install: pip install Pillow")
        return
    out_dir.mkdir(parents=True, exist_ok=True)
    for p in parties:
        r, g, b = p["color"]
        img = Image.new("RGBA", (seat_size, seat_size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        pad = 1
        draw.ellipse([pad, pad, seat_size - pad - 1, seat_size - pad - 1], fill=(r, g, b, 255))
        path = out_dir / f"{prefix}_seat_{p['id']}.tga"
        img.save(str(path), format="TGA")
        print(f"  [tga]  {path.name}")

    # Governing marker: gold star-like circle with white outline
    gm_size = 8
    img = Image.new("RGBA", (gm_size, gm_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([0, 0, gm_size - 1, gm_size - 1], fill=(255, 210, 50, 255))
    draw.ellipse([1, 1, gm_size - 2, gm_size - 2], fill=(255, 215, 0, 255))
    path = out_dir / f"{prefix}_gov_marker.tga"
    img.save(str(path), format="TGA")
    print(f"  [tga]  {path.name}")

# ─── Default config ───────────────────────────────────────────────────────────

DEFAULT_CONFIG = {
    "tag": "GER",
    "total_seats": 397,
    "parties": [
        {"id": "kpd",     "seats": 12, "governing": False,
         "color": [139, 30,  30]},
        {"id": "sapd",    "seats": 36, "governing": False,
         "color": [196, 72,  58]},
        {"id": "spd",     "seats": 71, "governing": False,
         "color": [220, 130, 120]},
        {"id": "fvp",     "seats": 52, "governing": False,
         "color": [217, 195, 106]},
        {"id": "zentrum", "seats": 60, "governing": True,
         "color": [120, 185, 100]},
        {"id": "dkp",     "seats": 65, "governing": True,
         "color": [75,  116, 168]},
        {"id": "drp",     "seats": 34, "governing": True,
         "color": [55,  85,  140]},
        {"id": "fkp",     "seats": 48, "governing": True,
         "color": [95,  140, 190]},
        {"id": "dnvp",    "seats": 19, "governing": False,
         "color": [47,  47,  53]},
    ],
    "diagram": {
        "width": 700, "height": 250, "rows": 6,
        "cx": 170, "cy": 220, "r_inner": 75, "r_outer": 165, "seat_size": None,
        "seat_order": "angle", "radial_order": "inner_to_outer",
        "layout_engine": "parliamentarch",
        "filling_strategy": "default",
        "span_angle": 180,
        "seat_radius_factor": 0.62,
    },
}

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    script_dir = Path(__file__).parent
    mod_root = script_dir.parent.parent

    cfg_path = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        script_dir / "parliaments" / "GER_default.yml"

    if HAS_YAML and cfg_path.exists():
        with open(cfg_path, encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        print(f"[parliament] Config: {cfg_path}")
    else:
        if not HAS_YAML:
            print("[WARN] PyYAML not found. Using built-in defaults.")
        elif not cfg_path.exists():
            print(f"[WARN] Config not found: {cfg_path}. Using built-in defaults.")
        cfg = DEFAULT_CONFIG

    d = cfg["diagram"]
    total = cfg["total_seats"]
    tag   = cfg.get("tag", "GER")
    parties = cfg["parties"]
    # Ensure color tuples
    for p in parties:
        if isinstance(p["color"], list):
            p["color"] = tuple(p["color"])

    print(f"[parliament] tag={tag}  seats={total}  rows={d['rows']}  parties={len(parties)}")

    positions = compute_seat_positions(
        total,
        d["rows"],
        d["cx"],
        d["cy"],
        d["r_inner"],
        d["r_outer"],
        d.get("seat_order", "angle"),
        d.get("radial_order", "inner_to_outer"),
        d.get("layout_engine", "auto"),
        d.get("filling_strategy", "default"),
        d.get("span_angle", 180),
    )

    seat_size = d.get("seat_size")
    if seat_size in (None, "auto"):
        seat_size = compute_auto_seat_size(
            d["rows"],
            d["r_outer"],
            d.get("seat_radius_factor", 0.62),
            d.get("layout_engine", "auto"),
        )
    seat_size = int(seat_size)

    prefix = f"{tag}_parliament"
    gfx_path       = mod_root / "interface" / f"{prefix}.gfx"
    decisions_path = mod_root / "interface" / f"{prefix}_decisions.gui"
    sg_path        = mod_root / "common" / "scripted_guis" / f"{prefix}_sg.txt"
    icon_dir       = mod_root / "gfx" / "interface" / "parliament"

    gfx_path.write_text(generate_gfx(parties, tag), encoding="utf-8")
    print(f"  [gfx]  {gfx_path.relative_to(mod_root)}")

    decisions_path.write_text(
        generate_decisions_gui(
            positions, parties,
            d["width"], d["height"], seat_size, d["cx"], d["cy"], tag
        ),
        encoding="utf-8",
    )
    print(f"  [gui]  {decisions_path.relative_to(mod_root)}")

    sg_path.write_text(generate_sg(total, parties, tag), encoding="utf-8")
    print(f"  [sg]   {sg_path.relative_to(mod_root)}")

    revert_countrypoliticsview(mod_root)

    generate_seat_icons(parties, seat_size, icon_dir, prefix)

    print("[parliament] Done!")


if __name__ == "__main__":
    main()
