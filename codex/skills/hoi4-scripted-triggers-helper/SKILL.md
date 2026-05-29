---
name: hoi4-scripted-triggers-helper
description: Create, search, and maintain reusable Tsareich2 HOI4 scripted triggers, including variable checks, collection/faction-related checks, and custom trigger tooltips.
---

# HOI4 Scripted Triggers Helper

Use this skill when repeated trigger logic should become a reusable scripted trigger.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for custom trigger tooltip localisation.
- Do not reuse external mod-specific IDs or examples.

## Search Roots

- Scripted triggers: `common/scripted_triggers/`
- Collections: `common/collections/`
- Factions: `common/factions/`
- Scripted localisation: `common/scripted_localisation/`
- Localisation: `localisation/japanese/`

## Search First

```bash
rg -n '^[A-Za-z_][A-Za-z0-9_]*\s*=\s*\{' common/scripted_triggers
rg -n -i -B 8 -A 12 'keyword|has_variable|check_variable|custom_trigger_tooltip' common/scripted_triggers common/collections common/factions common/scripted_localisation
```

## Basic Pattern

```hoi4
# Country scope
_tsr_is_stable_country = {
  check_variable = { stability_level >= 0.5 }
}
```

Use in a trigger block:

```hoi4
available = {
  _tsr_is_stable_country = yes
}
```

## Tooltip Pattern

```hoi4
_tsr_can_join_shared_project = {
  custom_trigger_tooltip = {
    tooltip = _tsr_can_join_shared_project_tt
    has_war = no
    is_subject = no
  }
}
```

Localisation:

```yaml
l_japanese:
 _tsr_can_join_shared_project_tt:0 "The country is independent and at peace."
```

## Variable and Relationship Examples

```hoi4
_tsr_has_project_stage = {
  has_variable = _tsr_project_stage
  check_variable = { _tsr_project_stage > 0 }
}

_tsr_same_faction_as_from = {
  FROM = { exists = yes }
  is_in_faction_with = FROM
}
```

## Review Checklist

- Confirm the trigger scope and caller scope.
- Keep tooltip text tied to the actual failing condition.
- Prefer one reusable trigger when the same condition appears in several focuses, decisions, events, or scripted GUI blocks.
- Avoid expensive broad scopes in frequent checks.
