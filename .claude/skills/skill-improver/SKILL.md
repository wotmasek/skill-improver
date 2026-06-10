---
name: skill-improver
description: >-
  Retrospectively analyze the task/session that just happened and turn the
  lessons into concrete improvements to existing Claude Code skills (or a draft
  of a new skill). Use when the user runs /skill-improver, asks to "improve
  skills", wants a retrospective on the work just done, wants to capture lessons
  learned into a skill, or wants to optimize a skill for token efficiency and
  output quality. ALWAYS asks for the user's own feedback first and treats it as
  the highest-priority signal. Proposes changes as a diff and waits for approval
  before editing any file.
---

# Skill Improver

A meta-skill. It looks back at what was just done and *how*, draws conclusions
about the process, and translates them into improvements to the skills that
shaped (or should have shaped) the work.

It never edits a skill silently. It **proposes** changes and waits for the
user's approval.

## Operating principles

- **User feedback wins.** The user's own feedback is the strongest signal.
  Always solicit it explicitly and weight it above your own observations. If
  your analysis conflicts with their feedback, follow their feedback and say so.
- **Evidence over opinion.** Every proposed change must trace back to something
  that actually happened in this session (a wrong turn, a re-run, a missing
  step, a wasted batch of tokens, an explicit correction from the user).
- **Propose, don't impose.** Present changes as a reviewable diff. Edit files
  only after the user approves.
- **Smaller and sharper.** Improvements should make skills *more* token-efficient,
  not less. Adding words is a cost — justify it, or cut something else.

## Workflow

### Step 1 — Collect the user's feedback first (highest priority)

Before analyzing anything, ask the user directly, e.g.:

> "Before I run the retrospective — do you have your own feedback on how this
> went? What felt slow, wrong, or annoying? Anything you'd want done
> differently next time?"

Capture their points verbatim as **priority findings**. These outrank anything
you discover on your own. If they have no feedback, continue — but never skip
the ask.

### Step 2 — Reconstruct what happened (retrospective)

Build a short, factual timeline of this session from the conversation context:

- What was the goal? Was it met?
- What path did the work take? Note detours, retries, dead ends, and rework.
- Where were tokens spent unnecessarily (re-reading files, redundant searches,
  oversized tool outputs, repeated explanations, work later thrown away)?
- Where did the user have to correct or redirect you?
- Which skill(s) were active, and did they actually fire when they should have?

If a stored transcript is needed for detail, session logs live under
`~/.claude/projects/<project>/`. Prefer the in-context conversation first; only
read transcript files if the context is insufficient.

### Step 3 — Identify the target skills

Default scope: project skills in `.claude/skills/`. Also accept a skill path
the user names explicitly. To list candidates:

- Look in `.claude/skills/*/SKILL.md` (project) and, if relevant, the skill the
  user points at.

For each finding from Steps 1–2, map it to either:
- an **existing skill** that should have prevented it, or
- a **gap** — a recurring pattern with no skill covering it (candidate for a new skill).

### Step 4 — Evaluate against the rubric

Score each target skill on the dimensions in
`reference/evaluation-rubric.md` (read it now). In short:

1. **Trigger / description accuracy** — would the description make the skill
   fire at the right time, and *not* at the wrong time? (Most common failure.)
2. **Instruction clarity** — unambiguous steps, right order, no gaps.
3. **Missing steps & anti-patterns** — add steps that were missing; add explicit
   "don't do X" warnings for mistakes that actually happened this session.
4. **Examples & counter-examples** — concrete "use when…" and "do NOT use when…".
5. **Token efficiency vs. output quality** — does the skill get a better result
   for fewer tokens? Look for: bloated instructions, content that belongs in a
   reference file (progressive disclosure), steps that cause re-reads or
   redundant tool calls.

### Step 5 — Produce proposals

For each target skill, write a proposal containing:

- **Finding** — what happened (cite the moment), and which feedback/observation
  it came from. Mark priority findings (from Step 1) clearly.
- **Change** — the exact edit, shown as a before/after or unified diff.
- **Why it helps** — tie it to trigger accuracy, clarity, missing-step,
  example, or token efficiency. State the expected effect ("should stop the
  skill from re-reading the whole file", etc.).

If a gap was found, draft a **new skill** using `reference/skill-template.md`
(read it when needed). Present it as a proposal too — do not create it unsolicited.

Keep proposals ranked: priority (user feedback) first, then highest-impact.

### Step 6 — Approve, then apply

Show the full set of proposals and ask the user which to apply (all / some /
none / modified). Only after approval:

- Edit the relevant `SKILL.md` / reference files.
- For a new skill, create `.claude/skills/<name>/SKILL.md`.
- Summarize what changed and what was deliberately left out.

Do not commit or push unless the user asks.

## Guardrails / anti-patterns

- Do **not** edit any skill before the user approves the proposals.
- Do **not** invent findings to justify a change — if the session was clean,
  say so and propose nothing.
- Do **not** make skills longer "to be safe." Every added line is a token cost
  paid on every future invocation; prefer cutting or moving detail to a
  reference file.
- Do **not** overwrite a user's intentional wording just because it's verbose —
  confirm if unsure.
- Keep the main `SKILL.md` of any skill lean; push depth into `reference/` files
  that are read on demand.

## Reference files

- `reference/evaluation-rubric.md` — the scoring dimensions and token-efficiency
  heuristics. Read in Step 4.
- `reference/skill-template.md` — structure and frontmatter for drafting a new
  skill. Read in Step 5 when proposing a new skill.
