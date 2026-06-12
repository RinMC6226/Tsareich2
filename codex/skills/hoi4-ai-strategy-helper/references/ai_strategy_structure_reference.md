# AI Strategy Structure Reference (Kaiserreich patterns)

Condensed from `common/ai_strategy/_documentation.md` and a survey of actual KR usage.
For the full token list with per-token examples, always read the repo doc first.

## Bundle lifecycle

| Block | Scope | Evaluated | Use for |
|---|---|---|---|
| `allowed` | country | once / rarely | static filters: `original_tag`, DLC checks |
| `enable` | country | periodically | dynamic activation: date, war, flags, focus |
| `abort` | country | periodically (while active) | deactivation condition |
| `abort_when_not_enabled = yes` | - | - | shorthand: deactivate when `enable` is false |
| `reversed = yes` | - | - | trigger runs in target-country scope; `id` names the applier |

KR house rule: every bundle has `abort` or `abort_when_not_enabled`; use
`abort = { always = no }` to mark intentionally permanent strategies.

## Targeting forms

```
ai_strategy = {
	type = <token>
	id = GER                  # tag / state id / region id / token, depending on type
	tag = GER                 # front/concentration tokens: country target (repeatable)
	state = 42                # repeatable
	strategic_region = 65     # repeatable
	area = western_europe     # AI area from common/ai_areas (repeatable)
	country_trigger = { ... } # scope: candidate country, FROM: us
	state_trigger = { ... }   # scope: state, FROM: enemy, FROM.FROM: us
	ratio = 0.25              # min ratio of front covered before strategy applies
	value = 100
}
```

## Most-used tokens in KR (by occurrence count)

| Token | ~Count | What it does |
|---|---|---|
| `front_unit_request` | 176 | +/-% units requested for matching fronts |
| `diplo_action_acceptance` | 146 | accept/refuse specific diplo actions (with `target = <action>`) |
| `conquer` | 103 | war target desirability |
| `front_control` | 92 | force/freeze front execution (`priority`, `execution_type`, `execute_order`) |
| `ignore_claim` | 90 | ignore claims on us by target |
| `invade` | 87 | naval invasion desire vs target (negative = never) |
| `antagonize` | 86 | hostility weight |
| `diplo_action_desire` | 84 | AI's own desire to take a diplo action |
| `build_building` | 78 | weighted construction pick (`id = <building>`, optional `target`) |
| `role_ratio` | 75 | production share per division/ship role |
| `dont_defend_ally_borders` | 66 | binary: skip ally fronts (`id = <ally>`) |
| `declare_war` | 59 | push actual war declaration |
| `area_priority` | 45 | theater-level priority by AI area |
| `research_weight_factor` | 37 | soft-steer research (vs `research_tech` = hard force) |
| `front_armor_score` | 36 | where armor divisions get assigned (negative for mountains/deserts) |
| `strategic_air_importance` | 35 | air priority per strategic region |
| `put_unit_buffers` | 29 | strategic reserve in given states for given areas |
| `template_prio` | 22 | division template upgrade priority |
| `operative_mission` | 23 | spy mission targeting |

## Signature KR patterns

**Global-negative + local-positive** (focus a continent-spanning AI on home):

```
ai_strategy = { type = front_unit_request  area = globally        value = -90 }
ai_strategy = { type = front_unit_request  area = western_europe  value = 90 }
```

**Hostility lock** (make two blocs never cooperate):

```
ai_strategy = { type = antagonize id = RUS value = 1000 }
ai_strategy = { type = diplo_action_acceptance target = market_access_rights id = RUS value = -1000 }
```

**Terrain-aware armor placement** (one bundle, many one-liners):

```
ai_strategy = { type = front_armor_score id = "SWI" value = -100 }
```

**Trigger-targeted de-prioritization** (no fixed tag list needed):

```
ai_strategy = {
	type = front_unit_request
	country_trigger = { NOT = { is_neighbor_of = FROM } }
	value = -50
}
```

**Division cap guard** (stop army production at the cap):

```
enable = { has_reached_maximum_divisions = yes }
ai_strategy = { type = build_army id = infantry value = -1000 }
```

## AI Areas (`common/ai_areas/default.txt`)

```
areas = {
	western_europe = {
		strategic_regions = { 1 2 3 ... }
	}
	asia = {
		continents = { asia india }
	}
	globally = {
		continents = { <all> }   # KR defines a "globally" area to enable the global-negative pattern
	}
}
```

Areas are referenced by `area_priority`, `front_unit_request`, `force_concentration_*`,
`put_unit_buffers`, `naval_dominance` etc. Define once, reuse everywhere.

## Faction theaters (`common/ai_faction_theaters/`)

Faction-wide theater definitions: which strategic regions form a theater, which
member countries should fight there, and when the theater stops existing.

```
reichspakt_western_europe = {
	name = <loc key>
	regions = { 5 6 7 ... }                # strategic regions
	can_skip_first_region = yes
	preferred_countries = { GER BEL HOL ... }
	cancel = { NOT = { has_war_with = INT } }   # INT = country being evaluated
	ai_will_do = { base = 0  modifier = { add = 100 original_tag = GER } }
}
```
