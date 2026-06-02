# Tsareich2 - AI Agent Guidelines

This repository contains the Tsareich2 Hearts of Iron IV mod. These instructions are shared by Codex, Claude, Gemini, GitHub Copilot, Opencode, and other AI coding agents.

## Required First Steps

- Read this file before making changes.
- Check the current branch and worktree state with `git status --short --branch`.
- Do not overwrite or revert user changes unless the user explicitly asks for it.
- Create or switch to an appropriate working branch before editing files.
- Do not push directly to `main`.

## GitFlow

Use `develop` as the integration branch. Finished work branches should be merged into `develop`, not `main`.

Branch names must use this format:

```text
type/scope_name
```

Allowed `type` values:

- `feature`: new content, systems, countries, map work, technology, UI, or documentation
- `fix`: bug fixes, crash fixes, syntax fixes, localisation fixes
- `archive`: saved historical versions or preservation branches

Scope examples:

- `TAG`: country tag work, such as `GER`, `JAP`, `RUS`
- `_map`: map, states, provinces, strategic regions
- `_Technology`: technologies and related equipment unlocks
- `_system`: shared systems, scripted effects, scripted triggers, GUI systems
- `crash_TAG`: crash fix for a specific country or feature

Examples:

```text
feature/GER_project
feature/_map_africa
feature/_system_parliament
feature/_system_ai_agent_guidelines
fix/crash_JAP_event
archive/1.0
```

When working on multiple unrelated items, switch branches for each item.

See `docs/gitflow.md` for the detailed policy.

## Project Layout

- `common/`: HOI4 gameplay definitions, scripted logic, focuses, ideas, decisions, AI, technologies
- `events/`: event files
- `history/`: starting state, countries, units, and related setup
- `interface/`: GUI definitions
- `gfx/`: graphics, sprites, flags, portraits
- `localisation/japanese/`: Japanese localisation
- `map/`: map data
- `music/`: music definitions and assets
- `tools/`: local helper tools
- `documents/`: HOI4 scripting references for coding agents and contributors
- `docs/`: development plans (`docs/plan/`), design docs, and worldbuilding/prehistory (`docs/prehistory/`). Not loaded by the game.

## Coding Agent Reference Path

Use `documents/README.md` as the entrypoint when you need HOI4 scripting context.

- Start with `documents/00_coding_contexts/script_concept_documentation.md` for script syntax and concepts.
- Use `documents/00_coding_contexts/effects_documentation.md` and `documents/00_coding_contexts/triggers_documentation.md` before writing effects or triggers.
- Use `documents/02_scopes/hoi4_scopes.json` and `documents/02_scopes/01_Dual scopes.md` when checking valid scopes.
- Use `documents/01_effects/effects.json` and `documents/04_triggers/triggers.json` for searchable effect and trigger data.
- Use `documents/00_character/` before changing character, leader, advisor, or trait definitions.
- Use `documents/95_scripted_localisation.md`, `documents/99_scripted_effects.md`, and `documents/99_scripted_triggers.md` for reusable HOI4 script patterns.

## Worldbuilding / Prehistory Reference

`docs/prehistory/` holds the mod's alternate-history prehistory (the story leading up to the 1936.1.1 start). Before implementing or revising a country, focus, event, idea, or decision, read the relevant prehistory so narrative and implementation stay consistent.

- Entry point: `docs/prehistory/README.md` — file format, the point of divergence, and how to read the archive.
- `docs/prehistory/TIMELINE.md` — backbone chronology from the point of divergence to 1936.
- `docs/prehistory/ENTITIES.md` — maps lore names to game IDs (TAG, character tokens, factions).
- `docs/prehistory/nations/<TAG>.md` — per-country prehistory for the TAG you are working on.
- Respect the `canon` field in each file: do not implement `proposed` lore as established fact.
- When you implement something, update the `implements:` field of the prehistory file that justifies it.
- `docs/prehistory/` is documentation only; the game does not load it. Keep it distinct from `documents/` (technical scripting references). Design/implementation plans live in `docs/plan/`.

## HOI4 Script Style

- Use 2 spaces for indentation.
- Do not use tabs.
- Keep one statement per line.
- Keep unrelated refactors out of feature branches.
- Match nearby file structure and naming before introducing new patterns.
- Prefer existing scripted effects, scripted triggers, variables, and localisation keys over duplicating logic.
- Keep high-frequency logic cheap: avoid broad scopes such as `any_state` in frequent triggers unless necessary.
- Put test/debug content in clearly named test or debug files.

## Naming

- Country-specific files should use a 3-letter tag prefix where appropriate, such as `GER.txt` or `JAP.txt`.
- Shared system files should use a clear system prefix, preferably `_tsr_` or an existing Tsareich2-local pattern.
- Test/debug files should be clearly marked with `_test`, `_debug`, or an existing local convention.
- New IDs should be unique and should not shadow vanilla or existing mod IDs.

## Localisation

- Primary localisation path: `localisation/japanese/*.yml`.
- Use `l_japanese:` as the header.
- Keep keys consistent with the script IDs they describe.
- Use `[?variable_name]` for dynamic variable display.
- Preserve existing encoding. For new Japanese localisation files, use UTF-8 with BOM when possible.
- If adding gameplay-visible content, add or update localisation in the same branch.

## Assets

- Do not modify `.wav` or `.ogg` files unless the user explicitly asks.
- Do not add secrets, local credentials, or publishing tokens.
- Optimize image assets before committing when possible.
- Keep asset names aligned with existing `gfx` and `interface` patterns.

## Validation

There is no single build step for the mod. Validate by the smallest practical method:

- Syntax and file inspection for script-only changes.
- HOI4 console tests such as `event <id> <TAG>`, `reload interface`, and `reload localisation` when available.
- For performance-sensitive changes, use `imgui show profiler` and inspect the Script tab, especially hourly processes.

If a validation step cannot be run locally, state that clearly in the final report.

## AI-Specific Notes

- Claude should also read `CLAUDE.md`.
- Gemini should also read `GEMINI.md`.
- GitHub Copilot should follow `.github/copilot-instructions.md`.
- Opencode should follow `.opencode/AGENTS.md`.
- Codex should treat this file as the primary repository instruction file.
