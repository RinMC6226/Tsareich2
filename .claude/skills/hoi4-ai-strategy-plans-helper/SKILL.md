---
name: hoi4-ai-strategy-plans-helper
description: Search, analyze, or author Hearts of Iron IV AI strategy plans (scripted national focus ordering, idea picks) and AI focuses (research weight profiles) using Kaiserreich patterns.
---

# HOI4 AI Strategy Plans & Focuses Helper

Use this skill for `common/ai_strategy_plans/` (scripted focus paths per political route) and `common/ai_focuses/` (research weight profiles). KR is a study reference; when porting, extract patterns, never KR-specific focus IDs or flags.

## Search Roots

- Focus plans: `common/ai_strategy_plans/<TAG>_strategy_plan.txt` (KR only writes plans for 9 majors: GER, FRA, RUS, JAP, TUR, RAJ, HND, SRI, CA)
- Research profiles: `common/ai_focuses/generic.txt` (defaults) + per-country files (`germany.txt`, `USA.txt`, ...)

## Common Searches

```bash
rg -n -B 2 -A 25 '^[A-Z]+_[a-z_0-9]+ = \{' common/ai_strategy_plans      # all plans with structure
rg -n 'has_country_flag = [A-Z]+_[a-z_]+_ai' common/ai_strategy_plans    # how plans branch on AI personality flags
rg -n -B 4 -A 12 'ai_national_focuses' common/ai_strategy_plans/GER_strategy_plan.txt
rg -n '^ai_focus_[a-z_]+' common/ai_focuses                              # all research profiles
```

## Strategy Plan Structure

```
GER_dkp_ai_plan = {
	name = "GER_dkp_ai_plan"          # optional display/loc name
	enable = {                        # when this plan governs the AI
		has_completed_focus = GER_conservative_revolution
		has_country_flag = GER_dkp_ai # KR pattern: political-path AI flag set at game start / by event
	}
	abort = { has_completed_focus = GER_the_reaction }   # usually: last focus of the list completed

	ai_national_focuses = {           # ORDERED list - AI picks the first available focus in it
		GER_ruhrkampf
		GER_conservative_revolution
		...
	}

	ideas = {                         # optional: weight bonuses for picking ideas/advisors
		low_economic_mobilisation = 10
		mitsui = 30
	}

	weight = { factor = 1.0 }         # keep ~1.0; also factors research needs. Higher = wins over overlapping plans
}
```

## KR Plan-Chaining Technique

KR splits one country's playthrough into several small plans chained by `enable`/`abort`:

1. **Starting plan** - `enable = { date > 1936.x.x has_country_flag = <route>_ai }`, short focus list, `abort` when the last focus completes.
2. **Political plan** - `enable = { has_completed_focus = <branch point> has_country_flag = <route>_ai }`, the full political path.
3. **Army plan** - `enable = { has_completed_focus = <political end> date > 1939.1.1 }`, military branch focuses gated behind a date.
4. **Wartime plan** - `enable = { has_war_with = X }` with high `weight` (e.g. 5.0) to override everything when war starts.

The AI personality flag (`GER_schleicher_ai`, `GER_dkp_ai`, ...) is the router: one flag per political route, set via game rules/events, each route gets its own plan chain.

## AI Focuses (research profiles)

`common/ai_focuses/generic.txt` defines the research weights of the hardcoded AI focus categories (`ai_focus_defense`, `ai_focus_aggressive`, `ai_focus_war_production`, `ai_focus_military_equipment`, `ai_focus_military_advancements`, `ai_focus_peaceful`, `ai_focus_naval`, `ai_focus_naval_air`, `ai_focus_aviation`):

```
ai_focus_naval = {
	research = {
		naval_doctrine = 100.0   # research category or tech tag = weight
		ss_tech = 8.0
	}
}
```

Country files override by suffixing the tag: `ai_focus_naval_GER = { research = { ... } }`. KR uses this to make e.g. Germany value carriers and battleships higher than generic countries.

## Pitfalls

- `ai_national_focuses` is an order preference, not a hard script: if a listed focus is unavailable, the AI takes the next listed one it can, and focuses outside the list can still be picked when nothing in the list is available - keep `abort` tight so stale plans don't linger.
- `weight` is also a factor on research needs - the repo comments recommend staying around 1.0 and reserving large values (3-5) for must-win situations like wartime plans.
- Plans need `allowed = { original_tag = X }` when the file is shared, otherwise every country evaluates `enable`.
- A plan list works best when every focus in it actually exists and is reachable on that route; verify with `rg 'focus_id' common/national_focus`.
