---
name: hoi4-modifier-maker
description: Build Tsareich2 Hearts of Iron IV modifier blocks for ideas, focuses, decisions, traits, dynamic modifiers, and scripted effects, with modifier lookup and balanced value checks.
---

# HOI4 Modifier Maker

Use this skill when constructing modifier blocks or dynamic modifiers for Tsareich2 gameplay content.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Verify modifier names with `hoi4-modifier-searcher` before writing unfamiliar modifiers.
- Prefer existing balance patterns in nearby ideas, focuses, decisions, traits, and dynamic modifiers.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Determine where the modifier will live:

- Static modifier inside an idea, focus reward, decision, trait, or scripted effect.
- Dynamic modifier under `common/dynamic_modifiers/` when values must change with variables or conditions.

2. Search for nearby balance and naming patterns:

```bash
rg -n -i -B 8 -A 24 'stability|war_support|factory|army|navy|air|modifier_id|keyword' common localisation/japanese
```

3. Verify modifier keys:

```bash
python3 codex/skills/hoi4-modifier-searcher/scripts/search_modifiers.py keyword
```

4. Choose static vs dynamic:

- Use static modifiers for fixed bonuses or penalties.
- Use dynamic modifiers for scaling, variable-based, or conditionally updated values.
- Avoid dynamic modifiers when a normal idea modifier is enough.

5. Build the block:

```hoi4
modifier = {
  stability_factor = 0.05
  political_power_gain = 0.10
}
```

6. For dynamic modifiers:

- Place in the closest existing `common/dynamic_modifiers/` file or a focused new file.
- Use a Tsareich2-local ID, preferably `_tsr_` for shared systems.
- Ensure the caller adds, removes, or updates the dynamic modifier deliberately.

7. Verify:

```bash
rg -n 'modifier_id|stability_factor|dynamic_modifier_id' common localisation/japanese
rg -n '\t' common localisation/japanese
```

## References

- Dynamic modifiers: `references/dynamic_modifier_guide.md`
- Modifier block templates: `references/modifier_templates.md`
