# GEMINI.md

This file provides Gemini-oriented guidance for working in the Tsareich2 Hearts of Iron IV mod repository.

Read `AGENTS.md` first. It is the shared instruction file for all AI agents and contains the required GitFlow and safety rules.

## Core Rules

- Check `git status --short --branch` before editing.
- Work only on a properly named branch.
- Never push directly to `main`.
- Merge completed branches into `develop`.
- Preserve user changes.
- Keep changes scoped to the request.

## Branch Naming

Use:

```text
type/scope_name
```

Examples:

```text
feature/GER_project
feature/_map_africa
feature/_system_ai_agent_guidelines
fix/crash_JAP_event
archive/1.0
```

See `docs/gitflow.md` for details.

## HOI4 Modding Rules

- Use 2 spaces and no tabs.
- Keep one statement per line.
- Match existing Tsareich2 patterns.
- Avoid expensive broad scopes in high-frequency triggers.
- Add localisation for visible gameplay content.
- Do not modify `.wav` or `.ogg` files unless explicitly requested.

## Localisation

- Use `localisation/japanese/*.yml`.
- Use `l_japanese:` headers.
- Preserve existing key naming and encoding patterns.
- Use `[?variable_name]` for variable display.

## Validation

Use the smallest relevant validation:

- Inspect changed files for syntax and scope consistency.
- Use `event <id> <TAG>` for event tests when possible.
- Use `reload interface` for GUI changes.
- Use `reload localisation` for localisation changes.
- Use `imgui show profiler` for performance-sensitive script changes.

If validation cannot be run, report that clearly.
