---
name: hoi4-on-actions-helper
description: Create or revise Tsareich2 Hearts of Iron IV on_actions, automatic event hooks, lifecycle handlers, war/diplomacy/state hooks, scoped effects, triggered events, and performance-sensitive recurring logic.
---

# HOI4 On Actions Helper

Use this skill when adding or changing Tsareich2 on_actions under `common/on_actions/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing on_action entries, scripted effects, scripted triggers, event namespaces, and localisation keys.
- Keep recurring hooks cheap, especially daily, weekly, monthly, and per-leader hooks.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Search existing handlers and nearby event wiring:

```bash
rg -n 'on_actions\s*=\s*\{|on_[A-Za-z0-9_]+\s*=\s*\{' common/on_actions
rg -n -i -B 10 -A 30 'on_action_name|keyword|event_id|scripted_effect' common/on_actions events common/scripted_effects common/scripted_triggers
```

2. Confirm hook scope and frequency:

- Check ROOT, FROM, and any special scope behavior for the chosen on_action.
- Treat `on_daily`, `on_weekly`, `on_monthly`, `on_army_leader_daily`, and similar loops as performance-sensitive.
- Prefer event dispatch or small scripted effects over inline large blocks.

3. Choose placement:

- Extend the closest existing file when the hook already exists or the system matches.
- Create a focused new file only when no current file fits.
- Use Tsareich2-local IDs; prefer `_tsr_` for shared system effects or triggers when appropriate.

4. Implement the smallest reliable hook:

```hoi4
on_actions = {
  on_startup = {
    effect = {
      _tsr_example_startup_effect = yes
    }
  }
}
```

5. If triggering events:

- Verify the event namespace and ID exist.
- Ensure the event type matches the on_action scope.
- Add localisation for any new visible event text.

6. Verify:

```bash
rg -n 'on_action_name|_tsr_example|event_id' common/on_actions events common/scripted_effects common/scripted_triggers localisation/japanese
rg -n '\t' common/on_actions events common/scripted_effects common/scripted_triggers localisation/japanese
```

## References

- On_action usage patterns: `references/usage_patterns.md`
- On_action reference notes: `references/on_actions_reference.md`
