---
name: hoi4-ai-design-principles
description: Architectural principles and effort-allocation strategy for Hearts of Iron IV AI modding, distilled from how the Kaiserreich team actually structures, disciplines, and prioritizes its 33k-line AI codebase. Use when planning or reviewing the AI layer of a mod, not when writing individual files.
---

# HOI4 AI Design Principles (Kaiserreich meta-lessons)

Use this skill when *planning* the AI architecture of a mod, deciding where to spend effort, or reviewing existing AI content for structural problems. For writing individual files, use the per-system skills (`hoi4-ai-strategy-helper`, `hoi4-ai-equipment-helper`, etc.).

## Principle 1: Build shared vocabulary BEFORE writing country logic

KR defines cross-cutting vocabularies once, then lets hundreds of entries reuse them:

- **Geography**: `common/ai_areas/` areas (including a `globally` all-world area) referenced by `area_priority`, `front_unit_request`, `put_unit_buffers`, `naval_dominance`...
- **Roles**: tokens like `infantry`, `naval_submarine` declared in `ai_templates`/`ai_equipment` and steered by `role_ratio`/`build_army` strategies. One token threads three systems.
- **AI personalities**: one country flag per political route (`GER_dkp_ai`, `GER_schleicher_ai`) set once, then used as the router by every strategy-plan chain.
- **Shared scripted triggers**: e.g. one `AI_trigger_can_upgrade_in_field` referenced by every template design, so policy changes happen in one place.

Review question: if a new country needs AI behavior, can it be written mostly by *referencing* existing vocabulary? If not, the vocabulary layer is too thin.

## Principle 2: Allocate effort where AI decisions decide games

KR's actual line counts (total ~33k lines):

| System | Lines | Share | KR's choice |
|---|---|---|---|
| ai_strategy | 18,313 | ~55% | 637 bundles, ~60 country files |
| ai_equipment | 10,115 | ~31% | every ship/plane generation designed |
| ai_strategy_plans | 1,982 | 6% | **only 9 countries** (GER, FRA, RUS, JAP, TUR, RAJ, HND, SRI, CA) |
| ai_templates | 1,276 | 4% | ~10 role-family files, world covered via blocked_for |
| ai_focuses / theaters / navy / areas | ~1,500 | 4% | generic + 7 major-country research overrides; navy = 3 generic files |

Lessons:
- Do NOT write focus plans for every country. Script only nations whose focus order decides the campaign; let `ai_will_do` handle the rest.
- Navy templates can stay generic; country flavor comes from production steering (role_ratio + equipment availability), not per-country fleet files.
- Major-country strategy files are dense (GER, RUS, FRA); minors may legitimately be a handful of diplomacy locks. Uneven depth is a feature, not neglect.

## Principle 3: Enforce lifecycle discipline mechanically

KR house rules observed across the codebase - adopt them as review criteria:

- Every strategy bundle has `abort` or `abort_when_not_enabled`; intentionally permanent ones say `abort = { always = no }` explicitly so the omission is never ambiguous.
- Static checks (`original_tag`, DLC) go in `allowed` (rarely evaluated); dynamic checks (date, war, flags) go in `enable`. Never date-check in `allowed`.
- Every strategic-region/state ID gets a name comment (`19 #Northern France`). IDs without comments rot.
- Every `blocked_for` tag list documents WHY each group is excluded (`#uses line_camelry instead`).
- Thresholds in progression ladders are staggered and commented (45/90/135 factories, set at ~90% of intended value to prevent flip-flopping).

## Principle 4: Keep knowledge in the repo, next to the code

KR maintains two first-party docs *inside* `common/`:

- `ai_strategy/_documentation.md` - full token list + examples, with an explicit "keep this up-to-date" header.
- `ai_equipment/_documentation_AI_ships_production_KR.info` - a practitioner's playbook: silent-failure traps, hierarchy explanation, in-game debug procedure (`aiview`, hot-reload loop).

When you discover an engine quirk (e.g. "bare `ship_medium_battery` category silently prevents the hull from ever being built"), write it into the in-repo doc immediately. KR even documents known-broken engine features in place (`preferred_countries` - "Behaviour a bit bugged - experiment with later") instead of leaving future maintainers to rediscover them.

## Principle 5: Design around the hardcoded AI, not against it

Recurring KR moves that respect engine behavior instead of fighting it:

- **Global-negative + local-positive** value stacking instead of trying to enumerate every front.
- **Zero-priority "recognition" entries** (militia template at `upgrade_prio base = 0`) so the AI classifies existing units into a role it will later upgrade out of.
- **Soft steering by default** (`research_weight_factor`, weighted plans ~1.0), hard forcing reserved for moments that must happen (`research_tech`, wartime plan `weight = 5.0`, value = 1000 diplomacy locks).
- **Tech/industry gates inside priority modifiers** (`factor = 0` conditions) rather than availability blocks, keeping designs visible to the AI's classifier.

## Known imperfections (calibrate your expectations)

KR is disciplined, not immaculate - do not cargo-cult everything:

- Comment density is ~6% and uneven; strategy-plan comments are copy-pasted boilerplate.
- Copy-paste slips exist (e.g. `ai_strategy/00_default.txt` has the same `pp_spend_priority id = relation` entry twice).
- `ai_focuses` country files duplicate near-identical blocks per puppet tag instead of sharing.

When auditing your own mod, grep for exact-duplicate `ai_strategy` entries and near-identical blocks as a cheap quality pass:

```bash
rg -N 'type = |id = |value = ' common/ai_strategy/<file> | uniq -d
```

## Planning checklist for a new mod's AI layer

1. Define `ai_areas` matching YOUR mod's strategic geography (include a `globally` area).
2. Decide the role token set; wire it through templates, equipment, and role_ratio before tuning values.
3. List the countries whose AI decides the campaign - those get strategy plans and dense strategy files; everyone else gets defaults.
4. Write the `00_` default layer first (area priorities, production baselines, garrison/PP defaults), country files second.
5. Create the in-repo `_documentation.md` on day one and record every engine quirk you hit.
6. Adopt the lifecycle rules from Principle 3 as PR review criteria.
