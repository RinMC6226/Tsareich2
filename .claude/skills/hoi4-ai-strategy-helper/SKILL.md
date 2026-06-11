---
name: hoi4-ai-strategy-helper
description: Create or revise Hearts of Iron IV AI strategy bundles using Kaiserreich patterns - diplomacy steering, front and force concentration control, garrison buffers, production ratios, research forcing, espionage, and AI areas.
---

# HOI4 AI Strategy Helper

Use this skill when writing `common/ai_strategy/` content (in this repo or when porting KR techniques into another mod). KR is the reference; extract patterns, never copy KR-specific tags, flags, or focus IDs into other mods.

## Required Context

- Read `common/ai_strategy/_documentation.md` first - it is the authoritative token list with examples, maintained by the KR team.
- Strategy structure quick reference: `references/ai_strategy_structure_reference.md` (in this skill).
- KR file conventions: `00_*.txt` for systemic/default behavior shared by all countries, `TAG.txt` for one country, lowercase region files (`china.txt`, `america.txt`, `central_asia.txt`) for regional groups.

## Bundle Skeleton

```
my_strategy_bundle = {
	allowed = { original_tag = GER }   # static, cheap filter - checked rarely
	enable = { date > 1938.1.1 }       # activation condition
	abort = { has_capitulated = yes }  # always include abort or abort_when_not_enabled
	# abort_when_not_enabled = yes     # alternative: deactivate when enable turns false

	ai_strategy = { type = <token> id = <target> value = <number> }
	ai_strategy = { ... }              # any number of entries
}
```

## Workflow

1. Pick the right token. Survey what KR uses for the same problem:

```bash
rg -n -B 8 -A 6 'type = <token>' common/ai_strategy
```

2. Put static checks (`original_tag`, `has_dlc`) in `allowed`, dynamic ones in `enable`. Always pair with `abort` or `abort_when_not_enabled`; if a strategy must never deactivate, write `abort = { always = no }` explicitly.

3. Choose targeting:
   - `id = TAG` / `id = <state/region id>` / `id = <token>` - fixed target (most tokens).
   - `area = <ai_area>` - geographic targeting via `common/ai_areas/`. Define areas once, reuse everywhere (`area_priority`, `front_unit_request`, `put_unit_buffers`).
   - `country_trigger` / `state_trigger` - dynamic targeting; scope is the candidate enemy/state, `FROM` is the applying country. Keep these triggers cheap.
   - `reversed = yes` - write the bundle in the *target's* file: trigger runs in other countries' scope, and `id` names the country that applies the strategy toward them (KR uses this to centralize "everyone reacts to GER" logic in `GER.txt`).

4. Remember values stack additively across active strategies of the same type and target. KR's signature pattern: a global negative baseline plus targeted positive offsets (e.g. `front_unit_request` with `area = globally value = -90`, then `+90` for home areas).

5. Diplomacy steering combo used throughout KR: `antagonize` + `diplo_action_acceptance` (negative) to make hostility stick, or `alliance`/`befriend`/`support` (negative) to block friendship paths. Use `value = 1000`-scale for hard locks, smaller values for tendencies.

6. Front control: `front_unit_request` for unit allocation, `front_control` (with `priority`, `execution_type = careful/balanced/rush/rush_weak`) to force or freeze pushes, `area_priority` for theater-level weight, `put_unit_buffers` for strategic reserves, `theatre_distribution_demand_increase` for a specific theater.

7. Production direction: `role_ratio` (works with `ai_templates` roles and `ai_equipment` roles), `unit_ratio`, `equipment_production_factor`, `equipment_production_min_factories_archetype`, `building_target`, `build_building`. Research forcing: `research_tech` (hard) vs `research_weight_factor` (soft).

8. Verify formatting and lifecycle:

```bash
rg -n 'enable = |abort' <changed file>      # every bundle has a lifecycle
rg -n 'type = ' <changed file>              # tokens spelled correctly (no validator will catch typos)
```

## Pitfalls

- A misspelled `type` token fails silently. Always copy token names from `_documentation.md`.
- `allowed` is evaluated only at startup/rare points - never put date or war checks there.
- Broad triggers (`any_state`, `every_country`) inside `enable`/`country_trigger` run often; keep them cheap or pre-compute with flags.
- For air, `unit_ratio` values are weights (default 0, unset = never built); for land/navy they are `100 + value` percentage adjustments.
- `role_ratio = 0` (or unset) disables production of a role but does NOT stop refitting; block refitting at the `ai_equipment` design level (`priority = 0`).

## References

- Full token list and examples: `common/ai_strategy/_documentation.md`
- Structure and KR usage notes: `references/ai_strategy_structure_reference.md`
