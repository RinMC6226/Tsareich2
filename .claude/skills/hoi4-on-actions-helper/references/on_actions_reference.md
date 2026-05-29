# On Actions Reference Notes

This is a compact reference for common HOI4 on_action categories. Always confirm scope against nearby usage before implementation.

## Lifecycle

- `on_startup`: once when a game starts or loads initial setup.
- `on_daily`: frequent country-level work; use strict gates.
- `on_weekly`: recurring country-level work; still performance-sensitive.
- `on_monthly`: recurring country-level work; preferred over daily when exact timing is not needed.

## War and Diplomacy

- `on_declare_war`: war declaration hook; usually attacker/defender scoped.
- `on_war`: war start hook.
- `on_capitulation`: capitulation hook.
- `on_peaceconference_started` and `on_peaceconference_ended`: peace conference hooks.
- `on_join_faction` and `on_leave_faction`: faction membership hooks.

## State and Territory

- `on_state_control_changed`: state controller changed; state scope is common.
- `on_annex`: annexation hook.
- `on_nuke_drop`: nuclear strike hook.

## Characters and Units

- `on_army_leader_daily`: very frequent per-leader hook; avoid expensive logic.
- `on_army_leader_won_combat` and `on_army_leader_lost_combat`: combat result hooks.
- `on_naval_invasion` and `on_paradrop`: special operation hooks.

## Validation

Search before adding:

```bash
rg -n 'on_action_name|on_[A-Za-z0-9_]+' common/on_actions
```

Check triggered events and effects:

```bash
rg -n 'event_id|scripted_effect_id' events common/scripted_effects common/on_actions
```
