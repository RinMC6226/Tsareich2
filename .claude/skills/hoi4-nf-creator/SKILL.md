---
name: hoi4-nf-creator
description: Create or revise Tsareich2 Hearts of Iron IV national focuses, focus tree placement, prerequisites, mutually exclusive branches, bypasses, rewards, AI weights, icons, and Japanese localisation.
---

# HOI4 National Focus Creator

Use this skill when adding or changing Tsareich2 national focuses under `common/national_focus/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Preserve the existing tree layout, focus ID prefixes, icon style, and reward style.
- Add or update visible text in `localisation/japanese/`.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Inspect the target tree and nearby focuses:

```bash
rg -n -A 18 'focus_tree\s*=\s*\{' common/national_focus
rg -n -i -B 25 -A 45 'id\s*=\s*TAG_|keyword|focus_id' common/national_focus
rg -n 'focus_id|TAG_' localisation/japanese
```

2. Choose placement and identity:

- Match the target tree's country restriction and ID prefix.
- Place using nearby `x` and `y` spacing; avoid disrupting existing layout.
- Set `icon` from existing project or vanilla-style focus icons.
- Use the local default `cost` pattern unless there is a gameplay reason not to.

3. Wire tree logic deliberately:

- `prerequisite` for required previous focuses.
- Multiple `prerequisite` blocks mean OR; multiple IDs in one block mean AND.
- `mutually_exclusive` for branch choices.
- `bypass` only when the focus should auto-complete as obsolete.
- `available` only when runtime gating is actually needed.

4. Implement rewards:

- Prefer existing scripted effects/triggers for repeated logic.
- Put player-visible custom tooltip keys in `localisation/japanese/`.
- Keep large or repeated reward logic in a scripted effect when it improves clarity.

5. Add AI behavior:

- Add `ai_will_do` when pathing matters.
- Keep AI conditions cheap and aligned with the branch's intended path.

6. Verify:

```bash
rg -n 'id\s*=\s*focus_id|focus_id:' common/national_focus localisation/japanese
rg -n '\t' common/national_focus localisation/japanese
```

## References

- Focus structure patterns: `references/nf_structure.md`
