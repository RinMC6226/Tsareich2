---
name: hoi4-ai-navy-helper
description: Search, analyze, or author Hearts of Iron IV naval AI scripting (ai_navy) - mission goals and priorities, fleet templates, and task force compositions, using Kaiserreich patterns.
---

# HOI4 AI Navy Helper

Use this skill for `common/ai_navy/` - the three-layer system deciding how the AI organizes its navy and assigns missions. KR is a study reference; extract patterns, not KR IDs.

## The Three Layers

1. **Goals** (`ai_navy/goals/goals_generic.txt`) - which naval objectives exist and their priority bands.
2. **Fleets** (`ai_navy/fleet/generic_fleet_templates.txt`) - which task forces compose a fleet for a goal.
3. **Task forces** (`ai_navy/taskforce/generic_taskforce_templates.txt`) - ship composition per task force and its mission.

Production of the ships themselves is steered separately by `role_ratio` strategies (`common/ai_strategy/00_naval_production.txt`) and `common/ai_equipment/` designs; strategic targeting (which seas matter) by `naval_dominance`, `naval_avoid_region`, `convoy_raiding_target`, `naval_invasion_focus` strategies in `common/ai_strategy/`.

## Common Searches

```bash
rg -n -B 1 -A 6 'objective_type' common/ai_navy/goals          # goal -> priority bands
rg -n -B 1 -A 12 'required_taskforces|optional_taskforces' common/ai_navy/fleet
rg -n -B 2 -A 20 'min_composition|optimal_composition' common/ai_navy/taskforce
rg -n -B 4 -A 8 'type = naval_dominance|naval_avoid_region|convoy_raiding_target|naval_mission_threshold' common/ai_strategy
```

## Structures

Goal:

```
generic_convoy_raiding = {
	objective_type = convoy_raiding   # hardcoded objective token
	min_priority = 3                  # priority band vs other goals
	max_priority = 7
}
```

Objective tokens used by KR: `naval_invasion_support`, `naval_invasion_defense`, `mines_sweeping`, `mines_planting`, `coast_defense`, `convoy_protection`, `convoy_raiding`, `naval_dominance`, `training`, `naval_blockade`.

Fleet template:

```
generic_dominance_fleet_1 = {
	required_taskforces = { StrikeForce_1 = 1  PatrolReconForce_1 = 2 }   # must exist to form fleet
	optional_taskforces = { StrikeForce_1 = 1  PatrolDominanceForce_CA_1 = 1 }  # added when ships available
}
```

Task force template:

```
StrikeForce_1 = {
	ai_will_do = { factor = 1 }
	mission = { naval_strike }            # naval_strike / naval_patrol / convoy_raiding / convoy_escort / mines_planting ...
	min_composition = { destroyer = { amount = 6 } }
	optimal_composition = {
		carrier = { amount = 2 }
		battleship = { amount = 3 }
		heavy_cruiser = { amount = 3 }
		light_cruiser = { amount = 3 }
		destroyer = { amount = 18 }
	}
}
```

## KR Techniques Worth Stealing

1. **Min vs optimal split.** `min_composition` is intentionally tiny (e.g. 6 DD for a strike force, 1 CL for patrol) so even small navies form working fleets; `optimal_composition` defines the endgame fleet the AI grows toward.
2. **`role = 4` in composition entries** - requires ships of a specific design role (KR uses it to force actual minelayer destroyers into `MineLaying_1` instead of plain DDs). Pairs with the role system in `ai_equipment`.
3. **Specialized patrol forces per capital type** (`PatrolDominanceForce_CA_1` with CAs, `..._BC_1` with BCs) so the dominance fleet absorbs whatever capital type the country actually builds.
4. **Few generic templates instead of per-country ones.** KR keeps one generic file per layer; country flavor comes from production steering (role_ratio + ai_equipment availability), not from per-country navy templates - much cheaper to maintain.
5. **Priority bands** (`min_priority`/`max_priority`) overlap deliberately so wartime context (threat, invasions) reorders goals within the bands instead of scripts micromanaging it.

## Pitfalls

- Ship type names in compositions (`destroyer`, `light_cruiser`, `battle_cruiser`, `submarine`, `carrier`, `battleship`, `heavy_cruiser`) must match unit mapping, not equipment archetypes.
- A `required_taskforces` entry the country can never build (e.g. carriers for a minor) means that fleet never forms - keep requirements minimal.
- This folder controls organization and missions only; if the AI "won't raid convoys", check it actually *has* raiding ships (role_ratio + ai_equipment) before touching goals.
