---
name: hoi4-event-searcher
description: Search and analyze Tsareich2 Hearts of Iron IV events by id, namespace, trigger, effect, event type, picture, or event-chain reference.
---

# HOI4 Event Searcher

Use this skill when looking for existing events or event chains in Tsareich2.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, nearby naming patterns, and `_tsr_` for shared system IDs when appropriate.
- Prefer `localisation/japanese/` for gameplay-visible localisation.
- Do not reuse external mod-specific IDs or examples.

## Search Roots

- Events: `events/`
- Localisation: `localisation/japanese/`
- Event pictures and sprite definitions: `interface/`, `gfx/`

## Common Searches

Find an event by ID:

```bash
rg -n -C 20 'id\s*=\s*EVENT_ID\b' events
```

Find a namespace and all events under it:

```bash
rg -n '^\s*namespace\s*=\s*NAMESPACE\b|id\s*=\s*NAMESPACE\.' events
```

Find events by type:

```bash
rg -n '^\s*(country_event|news_event|state_event)\s*=\s*\{' events
```

Find events using an effect or trigger:

```bash
rg -n -B 25 -A 8 'add_political_power|has_war|set_country_flag' events
```

Find automatically firing or triggered-only events:

```bash
rg -n -B 8 -A 12 'mean_time_to_happen\s*=\s*\{|is_triggered_only\s*=\s*yes' events
```

Trace event chains:

```bash
rg -n -B 20 -A 8 '(country_event|news_event|state_event)\s*=\s*\{[^}]*id\s*=' events
rg -n -C 20 'id\s*=\s*NEXT_EVENT_ID\b' events
```

Find event picture usage:

```bash
rg -n -B 8 -A 12 'picture\s*=\s*GFX_' events
rg -n 'GFX_report_event_name|texturefile' interface
```

## Review Checklist

- Identify namespace, event type, trigger, immediate effects, options, and follow-up events.
- Check localisation keys for title, description, and options in `localisation/japanese/`.
- If editing, inspect nearby event files first and add only narrowly scoped changes.
