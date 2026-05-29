# On Action Usage Patterns

Use these patterns as neutral HOI4 references. Adapt names and scope to nearby Tsareich2 code.

## Startup Setup

Use startup hooks for one-time initialization. Keep the hook small and delegate larger work to scripted effects.

```hoi4
on_actions = {
  on_startup = {
    effect = {
      _tsr_example_startup_effect = yes
    }
  }
}
```

## Recurring Checks

Daily, weekly, monthly, and per-leader hooks run often. Gate them tightly.

```hoi4
on_actions = {
  on_monthly = {
    effect = {
      if = {
        limit = { has_country_flag = _tsr_example_enabled }
        _tsr_example_monthly_effect = yes
      }
    }
  }
}
```

## Event Dispatch

Use event dispatch when the player-facing result belongs in an event.

```hoi4
on_actions = {
  on_declare_war = {
    events = {
      example_namespace.1
    }
  }
}
```

## Random Events

Use weighted random events only when randomness is desired.

```hoi4
on_actions = {
  on_weekly = {
    random_events = {
      90 = 0
      10 = example_namespace.2
    }
  }
}
```

## Safety Checklist

- Confirm ROOT/FROM scope for the hook.
- Keep broad loops out of frequent hooks.
- Prefer scripted effects for reusable work.
- Add localisation for any newly triggered visible event.
