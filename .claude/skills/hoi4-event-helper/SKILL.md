---
name: hoi4-event-helper
description: Create or revise Tsareich2 Hearts of Iron IV events, including country events, news events, state events, options, triggers, effects, event pictures, AI choice weights, and Japanese localisation.
---

# HOI4 Event Helper

Use this skill when adding or changing Tsareich2 events under `events/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing scripted effects, scripted triggers, event namespaces, event pictures, and localisation keys.
- Add or update visible text in `localisation/japanese/`.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Find nearby events and namespace patterns:

```bash
rg -n '^(country_event|news_event|state_event|unit_leader_event)\s*=\s*\{' events
rg -n '^\s*namespace\s*=' events
rg -n -i -B 8 -A 24 'keyword|TAG|namespace' events localisation/japanese
```

2. Choose the event type and scope:

- `country_event`: ROOT is the receiving country.
- `news_event`: shown broadly; keep triggers and visibility deliberate.
- `state_event`: ROOT is the state.
- `unit_leader_event`: ROOT is the leader.

3. Place the event in the closest existing file by country or system. Create a new file only when no current file fits.

4. Define the event narrowly:

- Use an existing namespace and the next available numeric ID.
- Add `title`, `desc`, and `picture` when player-visible.
- Give every `option` a localisation-backed `name`.
- Add `ai_chance` when AI choice behavior matters.
- Keep expensive broad scopes out of frequently triggered events.

5. Prefer reusable logic when effects or triggers repeat:

```bash
rg -n -i 'similar_effect|similar_trigger|keyword' common/scripted_effects common/scripted_triggers
```

6. Add localisation:

```yaml
l_japanese:
 namespace.1.t:0 "..."
 namespace.1.d:0 "..."
 namespace.1.a:0 "..."
```

7. Verify:

```bash
rg -n 'namespace\.1|namespace\s*=' events localisation/japanese
rg -n '\t' events localisation/japanese
```

## References

- Event type and scope details: `references/event_types_reference.md`
- Common event effects: `references/event_effects_reference.md`
- Event picture guidance: `references/event_pictures_reference.md`
