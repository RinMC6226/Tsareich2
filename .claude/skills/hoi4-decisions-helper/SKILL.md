---
name: hoi4-decisions-helper
description: Create or revise Tsareich2 Hearts of Iron IV decision categories and decisions, including visibility, availability, activation, costs, effects, AI weights, icons, and Japanese localisation.
---

# HOI4 Decisions Helper

Use this skill when adding or changing Tsareich2 decisions under `common/decisions/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing decision categories, icons, scripted effects, scripted triggers, and localisation keys.
- Add or update visible text in `localisation/japanese/`.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Search existing categories and similar decisions first:

```bash
rg -n '^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\{' common/decisions
rg -n -i -B 12 -A 30 'keyword|TAG|category|decision_id' common/decisions localisation/japanese
```

2. Choose placement:

- Add to the closest existing category when the topic matches.
- Create a new category only for a distinct player-facing decision group.
- Match nearby ID prefixes and file naming.

3. Keep decision conditions cheap:

- `visible`: broad gating for whether the player should see it.
- `available`: conditions to start it.
- `activation`: extra activation requirements when needed.
- Avoid broad scopes such as `any_state` or `every_country` in frequently evaluated checks unless necessary.

4. Define player-facing behavior:

- Use existing `icon` values where possible.
- Set `cost`, `days_remove`, `days_re_enable`, and `fire_only_once` intentionally.
- Put gameplay result in `complete_effect`.
- Add `ai_will_do` when AI use should be deterministic or weighted.

5. Reuse shared logic:

```bash
rg -n -i 'similar_effect|similar_trigger|keyword' common/scripted_effects common/scripted_triggers
```

6. Add localisation for category, decision, and tooltip keys in `localisation/japanese/`.

7. Verify:

```bash
rg -n 'decision_id|category_id|tooltip_key' common/decisions localisation/japanese
rg -n '\t' common/decisions localisation/japanese
```

## References

- Decision properties: `references/decision_properties_reference.md`
- Decision icon examples: `references/decision_icons_reference.md`
