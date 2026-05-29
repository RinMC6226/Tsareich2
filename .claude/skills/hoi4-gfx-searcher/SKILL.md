---
name: hoi4-gfx-searcher
description: Search Tsareich2 HOI4 sprite definitions in .gfx files, map sprite IDs to texture paths, reverse lookup image usage, and verify referenced files exist.
---

# HOI4 GFX Searcher

Use this skill when identifying images for ideas, events, decisions, GUI elements, or any `GFX_` sprite reference.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style and naming; do not reuse external mod-specific IDs or paths.
- Inspect existing `interface/` and `gfx/` patterns before adding new assets.

## Script

This skill includes `scripts/search_gfx.py`. Run it from this skill directory or pass the path directly:

```bash
python3 .claude/skills/hoi4-gfx-searcher/scripts/search_gfx.py --base . --id GFX_NAME
python3 codex/skills/hoi4-gfx-searcher/scripts/search_gfx.py --base . --path image_name
```

Options:

```bash
--base, -b <path>       Mod base directory, usually the Tsareich2 repo root
--interface, -i <path>  Interface directory, default <base>/interface
--id <name>             Search by sprite ID/name
--path, -p <path>       Search by texture path or filename
--exact, -e             Exact match instead of partial match
--limit, -l <number>    Maximum results, default 50
```

## Fast `rg` Searches

Find a sprite definition:

```bash
rg -n -B 4 -A 8 'name\s*=\s*GFX_NAME\b' interface
```

Find texture usage:

```bash
rg -n -i 'texture[fF]ile\s*=.*image_name|image_name' interface gfx
```

Find script references to a sprite:

```bash
rg -n 'GFX_NAME' common events interface localisation
```

## Review Checklist

- Record the sprite ID, `texturefile`, defining `.gfx` file, and whether the asset exists.
- Check case and extension carefully; HOI4 paths are often Windows-authored but the repo may be case-sensitive in tooling.
- When adding assets, align names with nearby Tsareich2 `gfx/interface/` and `interface/*.gfx` conventions.
