---
name: hoi4-scripted-effect-searcher
description: Search Tsareich2 common/scripted_effects for reusable HOI4 scripted effects by name, scope, keyword, tooltip, variable usage, or called effect.
---

# HOI4 Scripted Effect Searcher

Use this skill before creating or modifying scripted effects, and whenever the user asks what reusable effects already exist.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for tooltip localisation.
- Do not reuse external mod-specific IDs or examples.

## Search Root

- Scripted effects: `common/scripted_effects/`
- Localisation: `localisation/japanese/`

## Common Searches

List likely top-level effect definitions:

```bash
rg -n '^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\{' common/scripted_effects
```

Find a specific effect:

```bash
rg -n -C 30 '^\s*EFFECT_NAME\s*=\s*\{' common/scripted_effects
```

Find effects by operation:

```bash
rg -n -B 12 -A 8 'add_ideas|remove_ideas|add_political_power|set_variable|country_event' common/scripted_effects
```

Find tooltip and hidden-effect patterns:

```bash
rg -n -B 8 -A 12 'custom_effect_tooltip|hidden_effect\s*=\s*\{' common/scripted_effects
```

Find variable and array usage:

```bash
rg -n -B 8 -A 8 'set_variable|check_variable|add_to_array|for_each_loop' common/scripted_effects
```

Check callers of an effect:

```bash
rg -n '\bEFFECT_NAME\b' common events history
```

## Review Checklist

- Identify expected scope, side effects, tooltip behavior, localisation keys, and callers.
- Prefer reusing existing effects if semantics match.
- If creating a new effect, choose an existing Tsareich2 file by topic before adding a new file.
