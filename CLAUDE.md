# CLAUDE.md

This file provides Claude Code guidance for working in the Tsareich2 Hearts of Iron IV mod repository.

Always read `AGENTS.md` first. That file contains the shared rules for all AI agents, including GitFlow, branch naming, safety, style, and validation.

## Mod Overview

Tsareich2 is a Hearts of Iron IV mod repository. The project follows standard HOI4 mod structure with gameplay definitions in `common/`, events in `events/`, interface files in `interface/`, localisation in `localisation/`, map data in `map/`, and assets in `gfx/` and `music/`.

## Claude Workflow

Before edits:

- Run `git status --short --branch`.
- Confirm the work is on a properly named branch, such as `feature/_system_name` or `fix/crash_TAG_event`.
- If the task covers unrelated areas, split the work by branch.
- Inspect nearby files before creating new patterns.

During edits:

- Keep changes scoped to the request.
- Preserve user changes and unrelated work.
- Prefer existing Tsareich2 conventions over patterns from other repositories.
- Use concise comments only where the script is not self-explanatory.

After edits:

- Review changed files.
- Run the most relevant lightweight validation available.
- Report changed files and any validation that could not be run.

## HOI4 Development Rules

- Use 2 spaces, no tabs.
- Keep one script statement per line.
- Prefer existing scripted effects and triggers when adding reusable logic.
- Keep expensive scopes out of high-frequency scripted logic.
- Do not invent IDs or scopes when an existing project pattern is available.
- Keep debug/test content isolated and clearly named.

## Localisation

Primary localisation is Japanese:

```text
localisation/japanese/*.yml
```

Rules:

- Use `l_japanese:` headers.
- Keep keys aligned with event, focus, decision, idea, and GUI IDs.
- Add localisation with gameplay-visible script changes.
- Preserve existing encoding; use UTF-8 with BOM for new Japanese localisation files when possible.

## Common Task Guidance

### Events

- Use existing event namespace and ID conventions.
- Keep options and their effects clear.
- Add `ai_chance` where AI behavior should be deterministic or weighted.
- Add localisation for title, description, and options.

### Decisions

- Keep `available`, `visible`, `complete_effect`, and `ai_will_do` conditions cheap.
- Avoid repeatedly scanning broad scopes in mission-style decisions.
- Add localisation for category, decision, and tooltips.

### National Focuses

- Match existing focus tree structure and coordinates.
- Add `ai_will_do` when AI pathing matters.
- Keep prerequisites and mutually exclusive paths explicit.
- Add focus title and description localisation.

### Scripted Effects and Triggers

- Use shared files only for genuinely reusable logic.
- Name shared systems with a clear Tsareich2-local prefix, preferably `_tsr_` or an existing local pattern.
- Check scope assumptions carefully.

### GUI and Interface

- Match existing `.gui` and `.gfx` naming patterns.
- Validate with `reload interface` when possible.
- Keep localisation and scripted localisation in sync with visible GUI text.

### Map

- Use a dedicated branch such as `feature/_map_region`.
- Keep state, strategic region, province, and localisation changes grouped carefully.
- Record any manual game validation that was not possible.

## Worldbuilding / Prehistory

The mod's alternate-history prehistory (the story up to the 1936.1.1 start) lives in `docs/prehistory/`. Before adding or revising a country, focus, event, idea, or decision, read the relevant prehistory so the narrative and implementation stay consistent.

- Start at `docs/prehistory/README.md` (format, point of divergence, how to read), then `TIMELINE.md`, `ENTITIES.md`, and the relevant `nations/<TAG>.md`.
- Respect each file's `canon` field; do not implement `proposed` lore as established fact.
- After implementing, update the `implements:` field of the prehistory file that justifies it.
- `docs/prehistory/` is documentation only and is not loaded by the game. It is distinct from `documents/` (technical scripting references) and `docs/plan/` (design plans).

## External References

Use `bsm_test` and `SSW_mod` as reference repositories only for general HOI4 and AI-agent workflow patterns. Do not copy their mod-specific systems, tags, IDs, worldbuilding, or naval rules into Tsareich2 unless the user explicitly asks.

## Branch Policy

Claude must follow the branch policy in `docs/gitflow.md`:

- No direct push to `main`.
- Finished branches merge into `develop`.
- Start work on a branch.
- Switch branches between unrelated items.
- Use `type/scope_name` branch names.
