---
name: hoi4-scripted-localisation-helper
description: Create or revise Tsareich2 Hearts of Iron IV scripted localisation, defined_text blocks, conditional text, variable display, GUI text hooks, tooltips, and Japanese localisation keys.
---

# HOI4 Scripted Localisation Helper

Use this skill when adding or changing Tsareich2 dynamic text under `common/scripted_localisation/`.

## Required Context

- Read `AGENTS.md` before changing files.
- Follow `docs/gitflow.md`; work on a proper branch and do not edit on `main`.
- Preserve Tsareich2 style: 2 spaces, no tabs, one statement per line, nearby naming patterns.
- Prefer existing `defined_text` names, scopes, variable display patterns, and localisation keys.
- Add or update visible text in `localisation/japanese/`.
- Do not reuse external mod-specific IDs, tags, lore, or examples.

## Workflow

1. Search existing scripted localisation and callers:

```bash
rg -n 'defined_text\s*=\s*\{|name\s*=' common/scripted_localisation
rg -n -i -B 8 -A 16 'GetTextName|defined_text_name|keyword|\[\?variable' common interface localisation/japanese
```

2. Choose placement and name:

- Add to the closest existing scripted localisation file by system or topic.
- Create a new file only when no current file fits.
- Use a clear Tsareich2-local name; prefer `_tsr_` for shared systems when nearby conventions support it.

3. Confirm scope:

- Scripted localisation evaluates in the scope used by the caller, such as `[Root.GetName]`, `[This.GetName]`, or `[From.GetName]`.
- Check event, decision, focus, tooltip, or GUI caller scope before writing triggers.

4. Define text options:

```hoi4
defined_text = {
  name = GetExampleStatus

  text = {
    trigger = { has_war = yes }
    localization_key = example_status_war
  }

  text = {
    localization_key = example_status_peace
  }
}
```

5. Add a fallback `text` without a trigger unless the caller's trigger logic makes fallback impossible.

6. Add localisation:

```yaml
l_japanese:
 example_status_war:0 "..."
 example_status_peace:0 "..."
 example_tooltip:0 "[Root.GetExampleStatus]"
```

7. Verify:

```bash
rg -n 'GetExampleStatus|example_status_' common/scripted_localisation interface localisation/japanese
rg -n '\t' common/scripted_localisation interface localisation/japanese
```

## References

- Scripted localisation patterns: `references/scripted_loc_patterns.md`
- GUI integration notes: `references/gui_integration.md`
