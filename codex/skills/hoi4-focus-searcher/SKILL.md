---
name: hoi4-focus-searcher
description: Search and analyze Tsareich2 Hearts of Iron IV national focuses, focus trees, prerequisites, mutually exclusive branches, bypasses, AI weights, and completion rewards.
---

# HOI4 Focus Searcher

Use this skill when finding or explaining Tsareich2 national focus content.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for gameplay-visible localisation.
- Do not reuse external mod-specific IDs or examples.

## Search Roots

- Focus trees: `common/national_focus/`
- Localisation: `localisation/japanese/`
- Related scripted logic: `common/scripted_effects/`, `common/scripted_triggers/`

## Common Searches

Find a focus by ID:

```bash
rg -n -C 35 'id\s*=\s*FOCUS_ID\b' common/national_focus
```

Find focuses by tag or keyword:

```bash
rg -n -i -B 3 -A 20 'id\s*=\s*TAG_|keyword' common/national_focus
```

List focus tree definitions and country restrictions:

```bash
rg -n -A 18 'focus_tree\s*=\s*\{' common/national_focus
```

Find prerequisites and mutually exclusive links:

```bash
rg -n -B 8 -A 12 'prerequisite\s*=\s*\{|mutually_exclusive\s*=\s*\{' common/national_focus
```

Find bypass, available, cancel, and AI blocks:

```bash
rg -n -B 8 -A 18 'bypass\s*=\s*\{|available\s*=\s*\{|cancel_if_invalid\s*=|ai_will_do\s*=\s*\{' common/national_focus
```

Find focuses by completion reward effect:

```bash
rg -n -B 30 -A 8 'add_political_power|add_ideas|add_stability|country_event|hidden_effect' common/national_focus
```

Check localisation:

```bash
rg -n 'FOCUS_ID' localisation/japanese
```

## Review Checklist

- Identify tree ID, country restriction, focus position, prerequisites, mutually exclusive branches, bypass, rewards, and AI behavior.
- When adding or editing, preserve nearby focus layout and coordinate spacing.
- Prefer existing scripted effects and scripted triggers when reward or availability logic is repeated.
