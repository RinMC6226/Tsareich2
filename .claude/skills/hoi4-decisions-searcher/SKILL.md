---
name: hoi4-decisions-searcher
description: Search and analyze Tsareich2 Hearts of Iron IV decisions, decision categories, costs, triggers, missions, targeted decisions, and effects.
---

# HOI4 Decisions Searcher

Use this skill when finding or explaining decisions in Tsareich2.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for gameplay-visible localisation.
- Do not reuse external mod-specific IDs or examples.

## Search Roots

- Decisions: `common/decisions/`
- Categories: `common/decisions/categories/`
- Localisation: `localisation/japanese/`

## Common Searches

Find a decision or category by ID:

```bash
rg -n -C 30 '^\s*DECISION_ID\s*=\s*\{' common/decisions common/decisions/categories
```

Find decisions by keyword:

```bash
rg -n -i -B 8 -A 25 'keyword' common/decisions common/decisions/categories
```

Find availability, visibility, and effect blocks:

```bash
rg -n -B 8 -A 18 '^\s*(visible|available|complete_effect|remove_effect|timeout_effect)\s*=\s*\{' common/decisions
```

Find costs, cooldowns, timed decisions, and missions:

```bash
rg -n -B 8 -A 10 'cost\s*=|days_re_enable\s*=|days_remove\s*=|days_mission_timeout\s*=|is_good\s*=\s*yes' common/decisions
```

Find targeted or state-targeted decisions:

```bash
rg -n -B 10 -A 18 'target_trigger\s*=\s*\{|state_target\s*=\s*yes|target_root_trigger\s*=\s*\{' common/decisions
```

Find decisions by effect:

```bash
rg -n -B 25 -A 8 'add_stability|add_ideas|set_country_flag|country_event' common/decisions
```

Check localisation:

```bash
rg -n 'DECISION_ID|CATEGORY_ID' localisation/japanese
```

## Review Checklist

- Identify the category, visibility, availability, cost, completion effect, timeout behavior, cooldown, and AI usage.
- Verify category and decision localisation together.
- Before adding new decisions, inspect the existing file organization and choose the closest Tsareich2-local file.
