---
name: hoi4-ai-equipment-helper
description: Search, analyze, or author Hearts of Iron IV AI equipment designs (ai_equipment) - ship, tank, and plane variant design groups, module matching, refit control, and role-based production, using Kaiserreich patterns.
---

# HOI4 AI Equipment Designer Helper

Use this skill for `common/ai_equipment/` - the scripts that make the AI create equipment variants (ship/tank/plane designs), produce them, and refit/upgrade existing equipment. KR is a study reference; extract patterns, not KR IDs.

## Required Context

Two first-party docs live in the folder - read them before anything else:

- `common/ai_equipment/_documentation.md` - PDX syntax reference (design groups, target_variant, module matching operators).
- `common/ai_equipment/_documentation_AI_ships_production_KR.info` - KR's own playbook: the 3-level hierarchy, role_ratio vs unit_ratio, module-chaining tricks, and in-game debugging (`aiview`).

## Search Roots

- Ships: `KR_battleships.txt`, `KR_carriers.txt`, `KR_submarines.txt`, `KR_DD_*.txt`, `KR_light/heavy_cruisers.txt`, `generic_naval.txt`, `RUS_historical_designs.txt`
- Planes: `planes_*.txt` (fighter, cas, naval_bomber, cv_*, strategic, tactical, heavy, maritime patrol, scout)
- Tanks: `generic_tank.txt`
- Linked: `role_ratio` strategies in `common/ai_strategy/00_naval_production.txt`, `00_production*.txt`

## Common Searches

```bash
rg -n -B 2 -A 10 '^[a-zA-Z_]+ = \{' common/ai_equipment/KR_carriers.txt   # design groups in a file
rg -n 'roles = ' common/ai_equipment                                       # all role tokens
rg -n -B 4 -A 10 'type = role_ratio' common/ai_strategy                    # who produces which role
rg -n -B 2 -A 16 'target_variant' common/ai_equipment/planes_fighter.txt   # module layouts
rg -n -B 6 -A 4 'blocked_for|available_for' common/ai_equipment            # country gating
```

## The 3-Level Hierarchy (from KR's playbook)

1. **`ai_strategy` level** (`role_ratio`) - decides *what roles* get factories/dockyards. Does NOT stop XP spending or refits.
2. **Design group level** (`ai_equipment` top block) - one group per role (or several, e.g. BB + SHBB both serve `naval_capital_bb`). `priority = { base = 0 }` blocks production AND refits AND XP spend for the whole group.
3. **Design level** (named sub-blocks) - one per tech generation (`submarine_1936`, `submarine_1940`...). `priority` gates which generation is designed; `target_variant` defines the modules.

To block production: zero the `role_ratio`. To block refitting: zero the design `priority`.

## Design Skeleton

```
naval_submarine = {
	category = naval                  # naval / land (air uses the same system via planes_*)
	roles = { naval_submarine }       # token matched by role_ratio
	priority = { base = 10 }          # group priority, supports modifier blocks

	submarine_1940 = {
		role_icon_index = 6
		priority = {
			base = 35                 # KR ladder: 1922=0, 1936=20, 1940=35, 1944=50
			# modifier = { factor = 0 has_tech = <next hull> }  # common gate on planes/tanks
		}
		target_variant = {
			match_value = 3500.0      # how strongly existing ships match this design (for refits)
			type = ship_hull_submarine_3
			modules = {
				fixed_ship_engine_slot = sub_ship_engine     # category -> AI picks latest
				fixed_ship_torpedo_slot = ship_torpedo_sub
				mid_1_custom_slot = ship_sub_snorkel         # exact module -> hardcoded
			}
		}
	}
}
```

## Module Matching Operators (the part everyone gets wrong)

- `<slot> = <category>` - AI fits the latest researched module of that category. Default choice.
- `<slot> = <module>` - exact module only; use for modules without upgrades (e.g. `ship_mine_layer_1`).
- `<slot> > <module>` - anything better than this; for chains without a category (BB armor, `ship_light_medium_battery`).
- `<slot> = empty` - keep empty, strip installed modules on refit.
- Nested form with `any_of = { a b c }` - first listed is preferred. Chain fallbacks: `{ upgrade = current any_of = { engine_3 engine_2 engine_1 } }` - takes best available, and `upgrade = current` prevents costly refits of that slot.
- `requirements = { module = ship_mine_layer }` - hard gate so e.g. plain destroyers don't match the minelayer design.
- Every slot you want filled MUST be listed; unlisted slots stay empty forever.

## KR Pitfalls (from the .info file)

- If the AI has a newer hull tech, gate the older design with `modifier = { factor = 0 has_tech = <newer> }`, or it keeps building outdated designs.
- `match_value` only affects matching existing equipment for production/refit selection (100% all slots match, down to ~25%).
- `ship_medium_battery` as a bare category makes the AI never build the hull, with no error - use `>` or `any_of` for category-less modules.
- Too many active roles per country makes naval AI build unbalanced fleets; KR limits the role set per tag via `role_ratio` strategies.
- Live-tweak loop: pause, clear AI production lines, edit the file, save, unpause - ai_equipment hot-reloads without restarting.
- Debug in-game with the `aiview` console command; hovering ship designs shows the matched design group + score, or a red warning if no design matches.
