# New Skill Template

Use this when Step 5 identifies a gap worth a new skill. Draft it, present it as
a proposal, and only create the file after the user approves.

A skill is a directory `.claude/skills/<name>/` containing a `SKILL.md`. Deeper
material goes in `reference/` files that are read on demand.

## Frontmatter

```yaml
---
name: <kebab-case-name>
description: >-
  One or two sentences that say WHEN to use this skill — the concrete
  situations, user phrasings, and triggers. Include negative scope ("do NOT use
  when…") so it doesn't fire on lookalikes. This text is the only thing the
  model sees when deciding to load the skill, so make it specific about *when*,
  not just *what*.
---
```

Naming: `name` must be kebab-case and match the directory name.

## Body structure

Keep the body lean — every line is paid on each invocation.

```markdown
# <Skill Name>

One line on what this does and why it exists.

## When to use / when not to use
- Use when: <concrete trigger> 
- Do NOT use when: <lookalike that should be handled elsewhere>

## Workflow
### Step 1 — <action>
Concrete, ordered steps. Each step is an action, not an intention.

### Step 2 — <action>
...

## Guardrails / anti-patterns
- Do NOT <failure mode this skill must prevent>

## Reference files (optional)
- `reference/<x>.md` — read in Step N when <condition>.
```

## Checklist before proposing

- [ ] Is there really a recurring pattern, or was this a one-off? Only propose a
      skill for something likely to repeat.
- [ ] Does an existing skill already cover this? Improve that one instead.
- [ ] Is the description specific enough to fire at the right time and only then?
- [ ] Is the body as short as it can be while still unambiguous?
- [ ] Does any optional depth live in `reference/` instead of the main file?
