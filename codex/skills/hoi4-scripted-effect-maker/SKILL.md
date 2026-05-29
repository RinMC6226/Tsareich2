---
name: hoi4-scripted-effect-maker
description: Create or reuse small Tsareich2 HOI4 scripted effects with scope checks, existing-effect search, file placement, tooltip review, and localisation follow-through.
---

# HOI4 Scripted Effect Maker

Use this skill when the user asks to create a reusable scripted effect. Keep implementation narrow and reuse existing Tsareich2 logic whenever possible.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for tooltip localisation.
- Do not reuse external mod-specific IDs or examples.

## Workflow

1. Search existing effects first:

```bash
rg -n -i -B 12 -A 12 'keyword|similar_effect|operation_name' common/scripted_effects
rg -n '^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\{' common/scripted_effects
```

2. Choose a placement:

- Add to the closest existing file by topic.
- Create a new file only when no current file fits.
- Use `_tsr_` for shared system names when that matches nearby conventions.

3. Confirm scope:

- Country scope, state scope, character scope, or a deliberate nested scope.
- Check callers in focuses, decisions, events, history, or scripted GUI before deciding.

4. Decide tooltip behavior:

- Use `custom_effect_tooltip` when the player needs readable output.
- Put implementation-only work in `hidden_effect` only when the visible tooltip should be controlled.
- Add or update `localisation/japanese/` when a new tooltip key is introduced.

5. Implement minimally:

```hoi4
# Country scope
_tsr_example_effect = {
  custom_effect_tooltip = _tsr_example_effect_tt
  hidden_effect = {
    add_political_power = 50
  }
}
```

6. Verify:

```bash
rg -n '^\s*_tsr_example_effect\s*=\s*\{' common/scripted_effects
rg -n '_tsr_example_effect_tt' localisation/japanese
rg -n '\t' common/scripted_effects localisation/japanese
```

## Guardrails

- Do not duplicate an existing effect with only cosmetic naming differences.
- Do not move unrelated effects or reformat whole files.
- Keep broad loops such as `every_country`, `any_state`, and `every_owned_state` out of frequent logic unless there is a clear reason.
