---
name: hoi4-ai-strategy-searcher
description: Search and analyze Kaiserreich Hearts of Iron IV AI strategies, AI areas, and AI faction theaters - diplomacy weights, front control, production direction, area priorities, and theater assignments.
---

# HOI4 AI Strategy Searcher

Use this skill when finding or explaining AI behavior scripting in Kaiserreich under `common/ai_strategy/`, `common/ai_areas/`, and `common/ai_faction_theaters/`. This repository is a reference mod for studying AI modding techniques.

## Required Context

- This is the official Kaiserreich repository, used as a study reference. Do not edit files unless explicitly asked.
- When porting findings to another mod, do not copy KR-specific tags, focus IDs, flags, or lore - extract the *pattern*, not the content.
- First read `common/ai_strategy/_documentation.md` - it lists every strategy token with examples and is maintained by the KR team.

## Search Roots

- Strategy bundles: `common/ai_strategy/` (`00_*.txt` = defaults/systems, `TAG.txt` = per-country, region files like `china.txt`, `america.txt`)
- AI area definitions: `common/ai_areas/default.txt`
- Faction theaters: `common/ai_faction_theaters/ai_faction_theaters.txt`

## Common Searches

Find every use of a strategy type (e.g. `conquer`, `front_unit_request`, `role_ratio`):

```bash
rg -n -B 10 -A 6 'type = conquer' common/ai_strategy
```

Find how a specific country's AI is steered (its own file + mentions elsewhere):

```bash
rg -n -l 'id = GER|tag = GER' common/ai_strategy
rg -n -B 6 -A 12 'original_tag = GER' common/ai_strategy
```

Find a strategy bundle by name and inspect its lifecycle (`allowed`/`enable`/`abort`):

```bash
rg -n -A 20 '^bundle_name = \{' common/ai_strategy
```

Survey which strategy types KR uses most (great for learning priorities):

```bash
rg -ohN 'type = [a-z_]+' common/ai_strategy | sort | uniq -c | sort -rn | head -40
```

Find dynamic targeting via triggers instead of fixed IDs:

```bash
rg -n -B 6 -A 10 'country_trigger = \{|state_trigger = \{' common/ai_strategy
```

Find `reversed = yes` strategies (target-scope inversion technique):

```bash
rg -n -B 4 -A 16 'reversed = yes' common/ai_strategy
```

Find which AI areas exist and where they are referenced:

```bash
rg -n '^\t[a-z_]+ = \{' common/ai_areas/default.txt
rg -n 'area = |area_priority' common/ai_strategy
```

Find faction theater definitions and their AI weighting:

```bash
rg -n -B 2 -A 30 '^[a-z_]+ = \{' common/ai_faction_theaters
```

## Review Checklist

- For each bundle, identify: `allowed` (cheap static filter), `enable` (activation), `abort` or `abort_when_not_enabled` (deactivation), and the list of `ai_strategy` entries.
- Note whether targeting is by `id`/`tag` (fixed), by `area` (from `ai_areas`), or by `country_trigger`/`state_trigger` (dynamic).
- `reversed = yes` inverts applier and target: the trigger is evaluated in the scope of potential target countries, and the country named in `id` applies the strategy toward them.
- Values stack additively across active strategies of the same type/target (e.g. `conquer` + `avoid_starting_wars`).
- Check `00_default.txt`, `00_area_priority.txt`, `00_production.txt`, `00_factions.txt` for the baseline every country inherits before reading country files.
