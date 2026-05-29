---
name: hoi4-variable-helper
description: Guide Tsareich2 HOI4 variable, temp variable, array, collection, scripted localisation, faction, and constant usage with safe search-first workflows.
---

# HOI4 Variable Helper

Use this skill when working with HOI4 variables, arrays, collections, constants, or dynamic values in Tsareich2 scripts.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for player-facing variable display.
- Do not reuse external mod-specific IDs or examples.

## Search Roots

- Common script: `common/`
- Scripted effects/triggers: `common/scripted_effects/`, `common/scripted_triggers/`
- Collections: `common/collections/`
- Factions: `common/factions/`
- Scripted localisation: `common/scripted_localisation/`
- Localisation: `localisation/japanese/`

## Search First

```bash
rg -n -i -B 6 -A 8 'set_variable|set_temp_variable|check_variable|has_variable|clear_variable' common events history
rg -n -i -B 6 -A 8 'add_to_array|remove_from_array|is_in_array|for_each_loop|clear_array' common events history
rg -n -i -B 6 -A 8 'collection:|game:all_countries|country:faction_members|scripted_localisation' common
```

## Variable Basics

```hoi4
set_variable = { _tsr_project_progress = 0 }
add_to_variable = { _tsr_project_progress = 5 }
subtract_from_variable = { _tsr_project_progress = 1 }
clamp_variable = {
  var = _tsr_project_progress
  min = 0
  max = 100
}
check_variable = { _tsr_project_progress >= 50 }
clear_variable = _tsr_project_progress
```

Use temporary variables for calculations that should not be saved:

```hoi4
set_temp_variable = { _tsr_temp_score = industrial_capacity }
divide_temp_variable = { _tsr_temp_score = 10 }
```

## Arrays

```hoi4
clear_array = _tsr_candidate_countries
add_to_array = { _tsr_candidate_countries = ROOT }
is_in_array = { _tsr_candidate_countries = FROM }

for_each_loop = {
  array = _tsr_candidate_countries
  value = _tsr_current_candidate
  # Use _tsr_current_candidate inside the loop.
}
```

## Collections and Faction Data

Before adding collection or faction logic, inspect existing files:

```bash
rg -n -i 'collection|faction|member|leader' common/collections common/factions common/scripted_triggers common/scripted_effects
```

Prefer a named collection when the same filtered country or state set is reused by multiple systems.

## Localisation Display

```yaml
l_japanese:
 _tsr_project_progress_tt:0 "Progress: [?ROOT._tsr_project_progress]"
```

## Review Checklist

- Choose country, state, global, or temp storage deliberately.
- Prefix shared system variables consistently, usually with `_tsr_` when no closer local convention exists.
- Clear variables and arrays when the owning system ends.
- Avoid storing derived values permanently when they can be computed cheaply at use time.
