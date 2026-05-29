---
name: hoi4-modifier-searcher
description: Search Tsareich2 HOI4 modifiers, dynamic modifiers, and common vanilla-style modifier names by keyword or category when creating ideas, focuses, decisions, or scripted logic.
---

# HOI4 Modifier Searcher

Use this skill when choosing modifiers or inspecting dynamic modifiers in Tsareich2.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for gameplay-visible localisation.
- Do not reuse external mod-specific IDs or examples.

## Search Roots

- Static and idea modifiers appear in many files under `common/`.
- Dynamic modifiers: `common/dynamic_modifiers/`
- Modifiers directory: `common/modifiers/`

## Optional Helper Script

This skill includes `scripts/search_modifiers.py` as a convenience lookup for common vanilla-style modifier names. Treat it as a helper dictionary, not a complete source of truth for the current game version.

```bash
python3 .claude/skills/hoi4-modifier-searcher/scripts/search_modifiers.py --search stability
python3 codex/skills/hoi4-modifier-searcher/scripts/search_modifiers.py --category economy
python3 .claude/skills/hoi4-modifier-searcher/scripts/search_modifiers.py --list-categories
```

## Common Searches

Search existing Tsareich2 usage first:

```bash
rg -n -i -B 6 -A 8 'stability|war_support|production|consumer_goods|army_attack' common
```

Find dynamic modifier definitions:

```bash
rg -n '^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\{' common/dynamic_modifiers common/modifiers
```

Find dynamic modifiers by behavior:

```bash
rg -n -B 8 -A 12 'enable\s*=|remove_trigger\s*=|modifier\s*=\s*\{|state_' common/dynamic_modifiers common/modifiers
```

Find modifiers inside ideas, focuses, and decisions:

```bash
rg -n -B 8 -A 14 'modifier\s*=\s*\{' common/ideas common/national_focus common/decisions
```

## Review Checklist

- Verify whether a value is a factor, daily gain, absolute value, or percentage-like decimal.
- Prefer existing Tsareich2 modifier patterns and balance ranges.
- If unsure whether a modifier exists in the current HOI4 version, verify against game files or official/current references before implementing.
