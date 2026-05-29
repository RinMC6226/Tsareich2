# Opinion Modifier Usage Patterns

Use these neutral patterns as references and adapt IDs to Tsareich2 conventions.

## Static Positive Modifier

```hoi4
opinion_modifiers = {
  example_good_relations = {
    value = 25
  }
}
```

Apply it:

```hoi4
add_opinion_modifier = {
  target = FROM
  modifier = example_good_relations
}
```

## Temporary Decaying Modifier

```hoi4
opinion_modifiers = {
  example_recent_support = {
    value = 40
    months = 12
    decay = 3
  }
}
```

## Negative Modifier

```hoi4
opinion_modifiers = {
  example_diplomatic_insult = {
    value = -35
    months = 18
    decay = 2
  }
}
```

## Removal

```hoi4
remove_opinion_modifier = {
  target = FROM
  modifier = example_good_relations
}
```

## Checklist

- Confirm ROOT/FROM or explicit `target` scope.
- Add localisation for the modifier ID.
- Use decay for short-lived diplomatic effects.
- Avoid `trade = yes` unless the modifier intentionally affects trade.
