---
name: hoi4-opinion-modifiers-helper
description: Create or revise Tsareich2 Hearts of Iron IV opinion modifiers, diplomatic relation changes, temporary or decaying opinion effects, trade restrictions, trust bounds, usage hooks, and Japanese localisation.
---

# HOI4 Opinion Modifiers Helper

Use this skill when adding or changing Tsareich2 opinion modifiers under `common/opinion_modifiers/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing opinion modifier files, diplomatic scripted effects, events, decisions, and localisation keys.
- Add or update visible text in `localisation/japanese/`.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Search existing modifiers and callers:

```bash
rg -n 'opinion_modifiers\s*=\s*\{|^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\{' common/opinion_modifiers
rg -n -i -B 10 -A 24 'opinion_modifier_id|add_opinion_modifier|remove_opinion_modifier|keyword' common events history localisation/japanese
```

2. Choose placement and naming:

- Add country-specific modifiers to the closest country or topic file.
- Create a new file only when no current file fits.
- Match nearby Tsareich2 ID prefixes.

3. Define mechanics deliberately:

```hoi4
opinion_modifiers = {
  example_modifier = {
    value = 25
    months = 12
    decay = 2
  }
}
```

- Use positive values for improved opinion and negative values for worsened opinion.
- Add `months`, `years`, or `days` plus `decay` only for temporary effects.
- Add `trade = yes` only when the modifier should affect trade behavior.
- Use trust bounds only when the system explicitly needs them.

4. Wire usage:

- Apply with `add_opinion_modifier = { target = TAG modifier = opinion_modifier_id }`.
- Remove deliberately if the modifier is not meant to expire naturally.
- Check ROOT/FROM scope in events, decisions, and scripted effects before wiring.

5. Add localisation:

```yaml
l_japanese:
 opinion_modifier_id:0 "..."
```

6. Verify:

```bash
rg -n 'opinion_modifier_id|add_opinion_modifier|remove_opinion_modifier' common events history localisation/japanese
rg -n '\t' common/opinion_modifiers localisation/japanese
```

## References

- Opinion mechanics: `references/opinion_mechanics.md`
- Common usage patterns: `references/usage_patterns.md`
