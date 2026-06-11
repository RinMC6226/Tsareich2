---
name: hoi4-ai-templates-helper
description: Search, analyze, or author Hearts of Iron IV AI division template design (ai_templates) - roles, upgrade priorities, target templates, and factory-count-gated template progression, using Kaiserreich patterns.
---

# HOI4 AI Templates Helper

Use this skill for `common/ai_templates/` - the scripts that control which division templates the AI designs, upgrades, and fields. KR is a study reference; extract patterns, not KR tags.

## Search Roots

- `common/ai_templates/` - one file per role family: `infantry_default.txt`, `armour.txt`, `cavalry.txt`, `camelry.txt`, `irregulars.txt`, `marines.txt`, `mountaineers.txt`, `suppression.txt`, `infantry_artillery_focus*.txt`
- Linked systems: `role_ratio` / `template_prio` / `build_army` strategies in `common/ai_strategy/`, `AI_trigger_can_upgrade_in_field` in `common/scripted_triggers/`

## Common Searches

```bash
rg -n -B 2 -A 8 'blocked_for|available_for' common/ai_templates        # which countries use which template line
rg -n -B 2 -A 14 'target_template' common/ai_templates/armour.txt      # actual division compositions
rg -n -B 6 -A 10 'upgrade_prio' common/ai_templates                    # progression gating logic
rg -n 'role = ' common/ai_templates                                    # role tokens (link to role_ratio strategies)
rg -n -B 4 -A 8 'type = template_prio|type = role_ratio|type = build_army' common/ai_strategy
```

## Structure

```
line_infantry = {                       # template group (one per role per country-set)
	blocked_for = { TRP ETS ... }       # countries using another line instead (KR comments why)
	role = infantry                     # role token - matched by role_ratio/build_army strategies

	upgrade_prio = { base = 5 }         # group-level priority vs other groups

	infantry_default = {                # one design within the group
		upgrade_prio = {
			base = 1
			modifier = { factor = 0  num_of_military_factories < 45 }   # gate by industry
			modifier = { add = 1     has_reached_maximum_divisions = yes }
		}
		can_upgrade_in_field = { AI_trigger_can_upgrade_in_field = yes }
		target_template = {
			regiments = { infantry = 9  artillery_brigade = 1 }
			support   = { artillery = 1 anti_air = 1 engineer = 1 logistics_company = 1 field_hospital = 1 }
		}
	}
}
```

## KR Techniques Worth Stealing

1. **Industry-gated progression ladder.** Each better template (`infantry_default` → `infantry_upgraded` → `infantry_motorised` → `infantry_mechanised`) zeroes itself below a factory threshold (`modifier = { factor = 0 num_of_military_factories < N }`, where N is ~90% of the intended threshold) and gains weight when `has_reached_maximum_divisions = yes`. Result: poor AIs keep cheap templates, rich AIs upgrade automatically.
2. **Tech gates inside priorities.** `modifier = { factor = 0 NOT = { has_tech = mechanised_infantry } }` rather than `enable` blocks - keeps designs visible to the AI for recognition while unbuildable.
3. **Zero-prio recognition entries.** `infantry_irregular`/`infantry_militia` with `upgrade_prio = { base = 0 }` and a comment "only here so the AI recognises irregulars as part of the infantry line" - the AI then knows starting irregular divisions belong to this role and will upgrade them away.
4. **Country-set segregation via `blocked_for`.** One default file plus specialized lines (`line_cavalry`, `line_camelry`, `line_irregulars`, `infantry_artillery_focus`) - each country appears in exactly one line's block-list logic. Comments document the mapping.
5. **Shared field-upgrade trigger.** All designs reference one scripted trigger (`AI_trigger_can_upgrade_in_field`) so the global field-upgrade policy is editable in one place.

## Pitfalls

- A country in `blocked_for` of every group for a role will never design that role; keep the mapping exhaustive and documented.
- `role` tokens must match what `role_ratio`/`build_army` strategies and (for equipment) `ai_equipment` roles use, or production weighting silently does nothing.
- `target_template` regiment/support names are unit types from `common/units/` - typos fail silently.
- Keep thresholds consistent between designs (KR staggers 45/90/135 factories) or the AI flip-flops between templates and wastes army XP.
