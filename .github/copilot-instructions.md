# GitHub Copilot Instructions for Tsareich2

Follow the repository rules in `AGENTS.md`.

## Required Behavior

- Do not suggest direct pushes to `main`.
- Use work branches named `type/scope_name`.
- Finished work should be merged into `develop`.
- Keep suggestions consistent with existing Tsareich2 HOI4 script patterns.
- Do not modify `.wav` or `.ogg` files unless explicitly requested.

## Branch Examples

```text
feature/GER_project
feature/_map_africa
feature/_system_parliament
fix/crash_JAP_event
archive/1.0
```

## HOI4 Script Style

- 2 spaces, no tabs.
- One statement per line.
- Prefer existing scripted effects, scripted triggers, and naming conventions.
- Keep high-frequency logic performant.
- Add Japanese localisation for visible gameplay content.

## Localisation

- Path: `localisation/japanese/*.yml`
- Header: `l_japanese:`
- Use `[?variable_name]` for variable display.
- Keep localisation keys aligned with script IDs.
