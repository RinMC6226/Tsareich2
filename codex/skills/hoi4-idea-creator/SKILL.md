---
name: hoi4-idea-creator
description: Create or revise Tsareich2 Hearts of Iron IV national spirits and ideas, including idea definitions, modifiers, GFX sprites, idea pictures, usage hooks, and Japanese localisation.
---

# HOI4 Idea Creator

Use this skill when adding or changing Tsareich2 ideas under `common/ideas/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing idea files, GFX sprites, idea images, modifiers, and localisation keys.
- Add or update visible text in `localisation/japanese/`.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Search existing ideas and GFX first:

```bash
rg -n -i -B 8 -A 28 'idea_id|keyword|TAG_' common/ideas interface localisation/japanese
rg -n 'spriteType\s*=\s*\{|name\s*=\s*"GFX_idea_' interface
find gfx/interface -type f | rg -i 'ideas|idea|TAG|keyword'
```

2. Choose placement:

- Add country-specific ideas to the closest existing country or topic file.
- Create a new file only when no current file fits.
- Keep idea IDs aligned with nearby Tsareich2 patterns.

3. Define the idea:

- Use the correct category, usually `country` for national spirits.
- Use `picture = name_without_GFX_idea_prefix`.
- Add `allowed`, `available`, `cost`, or `removal_cost` only when needed.
- Build modifiers with `hoi4-modifier-searcher` and `hoi4-modifier-maker` when modifier names or values are uncertain.

4. Wire GFX:

- Reuse an existing sprite when it fits.
- If adding a sprite, define `GFX_idea_<id>` in an appropriate `.gfx` file and point it at an existing or newly supplied texture.
- Keep asset paths aligned with nearby `gfx/interface/ideas/` patterns.

5. Wire usage:

- If the idea is granted by focus, decision, event, or history, update that caller and ensure removal or replacement behavior is intentional.

6. Add localisation:

```yaml
l_japanese:
 idea_id:0 "..."
 idea_id_desc:0 "..."
```

7. Verify:

```bash
rg -n 'idea_id|GFX_idea_idea_id|idea_id_desc' common/ideas interface localisation/japanese
rg -n '\t' common/ideas interface localisation/japanese
```

## References

- Idea structure details: `references/idea_structure.md`
