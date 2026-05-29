# Opinion Modifier Mechanics

Opinion modifiers adjust diplomatic opinion between countries. Values are usually kept within the normal HOI4 opinion range.

## Core Fields

```hoi4
opinion_modifiers = {
  modifier_id = {
    value = 25
    months = 12
    decay = 2
    trade = no
  }
}
```

- `value`: positive improves opinion; negative worsens opinion.
- `months`, `years`, `days`: duration-related fields.
- `decay`: amount removed over the duration interval.
- `trade`: use only for trade-impacting modifiers.
- `min_trust` / `max_trust`: use only for systems that explicitly depend on trust.

## Duration Guidance

- Permanent: omit duration and decay.
- Temporary: set duration and decay.
- Event memory: use moderate values and gradual decay.
- Major diplomatic break: use larger negative values and longer duration.

## Scope Guidance

Typical usage:

```hoi4
add_opinion_modifier = {
  target = FROM
  modifier = modifier_id
}
```

Check the caller scope before choosing `ROOT`, `FROM`, a tag, or an event target.

## Localisation

```yaml
l_japanese:
 modifier_id:0 "..."
```
