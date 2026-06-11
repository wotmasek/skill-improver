---
name: skill-improver
description: >-
  Retrospectively analyze the task/session that just happened and turn the
  lessons into concrete improvements to existing Claude Code skills (or a draft
  of a new skill). Use when the user runs /skill-improver, asks to "improve
  skills", wants a retrospective on the work just done, wants to capture lessons
  learned into a skill, or wants to optimize a skill/process for token
  efficiency and output quality. ALWAYS asks for the user's own feedback first
  and treats it as the highest-priority signal, then runs its own first-
  principles analysis of the process. Proposes changes as a diff and waits for
  approval before editing any file.
---

# Skill Improver

A meta-skill. It looks back at what was just done and *how*, draws its own
conclusions about the process, and translates them into improvements to the
skills (and adjacent mechanisms) that shaped — or should have shaped — the work.

Two engines feed it:
1. **User feedback** — the highest-priority signal (always solicited first).
2. **First-principles process analysis** — its own rigorous, autonomous search
   for optimization, independent of whether the user flagged anything.

It never edits silently. It **proposes** changes and waits for approval.

## Operating principles

- **User feedback wins.** Solicit it explicitly and weight it above your own
  findings. If your analysis conflicts with their feedback, follow the feedback
  and say so.
- **But never stop at feedback.** Always run the autonomous process analysis
  (`reference/process-analysis.md`). Extract the maximum signal — relentlessly
  hunt for what to delete, simplify, reorder, automate, or cache.
- **Evidence over opinion.** Every proposed change traces to something that
  actually happened this session (a wrong turn, a re-run, a missing step, wasted
  tokens, an explicit correction).
- **Restraint, not drama.** Optimize hard, but do not cause drastic evolution.
  The modification level (below) caps how far any single run may go.
- **Smaller and sharper.** Adding words is a cost paid on every future load.
  Justify additions or cut something else. Enforce the length mechanism
  (`reference/length-and-structure.md`).
- **Propose, don't impose.** Present a reviewable diff; edit only after approval.

## Workflow

### Step 1 — Collect the user's feedback first (highest priority)

Before analyzing anything, ask directly, e.g.:

> "Before I run the retrospective — do you have your own feedback on how this
> went? What felt slow, wrong, or annoying? Anything you'd want done
> differently next time?"

Capture their points verbatim as **priority findings** — they outrank your own.
Also read their tone for severity (see Step 3). If they have no feedback,
continue — but never skip the ask.

### Step 2 — Run both retrospective engines

First reconstruct a short, factual timeline (goal, path, detours, retries, dead
ends, rework, where you were corrected, which skills fired or failed to fire).

Then run the **first-principles process analysis** — read
`reference/process-analysis.md` and apply its six lenses (question the
requirement → delete → simplify → reorder → automate → cache) with the relevance
bar. Produce autonomous findings that stand on their own, separate from feedback.

### Step 3 — Determine the modification level from severity

The level is a **cap on how far proposals may go**, derived from how the process
actually went (feedback + your severity read), not chosen arbitrarily.

- **Went well** (smooth, minor nits) → **L1 Surgical**: only changes with strong
  direct evidence; minimal diffs (fix a description line, add one warning, fix
  one ambiguous step). No restructuring.
- **Mediocre** (some rework/detours, fixable friction) → **L2 Structural**
  *(default)*: L1 + reorganize, split into references, add examples/counter-
  examples, light condensing, fix step order. No change to what the skill does.
- **Went badly** (significant wasted effort, repeated corrections, wrong
  outcomes) → **L3 Deep**: L2 + first-principles consolidation, merging
  redundant steps, rethinking the workflow.

The level is a ceiling, not a quota — even at L3, change only what the evidence
warrants. When severity is unclear, default to **L2**.

**Deep-change gate:** changing a skill's *purpose, scope, or behavior* ("what
the skill is") is allowed only at L3 **and** only behind a separate, explicit
second approval. Flag such proposals distinctly; without that extra "yes" they
stay behavior-preserving.

### Step 4 — Identify targets

Default scope: project skills in `.claude/skills/*/SKILL.md`, plus any skill the
user names. Map each finding to either an **existing skill** that should have
prevented it, or a **gap** (recurring pattern with no skill → candidate new
skill, use `reference/skill-template.md`).

Process findings may also point **beyond skills** — a hook, a slash command, a
settings change. You may propose these, and (after approval) implement them too,
not just skill files.

### Step 5 — Evaluate targets and apply length hygiene

Score each target skill against `reference/evaluation-rubric.md` (trigger
accuracy, instruction clarity, missing steps/anti-patterns, examples, token
efficiency).

For every target you touch, apply `reference/length-and-structure.md`: if a
`SKILL.md` approaches ~200 lines (or holds optional/rarely-needed detail),
propose extracting it into `reference/` files with clean navigation; apply
**light** condensing that removes redundancy only and never drops an
instruction, warning, or step.

### Step 6 — Produce proposals

For each: **Finding** (what happened + evidence; mark priority findings from
Step 1 and which lens autonomous ones came from) → **Change** (before/after or
unified diff) → **Level** it requires (L1/L2/L3; flag any deep-change-gate item)
→ **Why it helps** (trigger / clarity / missing-step / example / token cost) and
expected effect. Rank: priority feedback first, then highest-impact.

If the session was genuinely clean, say so and propose little or nothing.

### Step 7 — Approve, then apply

Show the full proposal set and ask which to apply (all / some / none /
modified). Deep-change-gate items need their own explicit yes. Only after
approval: edit the skill / reference files (and any approved hook / command /
settings), then summarize what changed and what was deliberately left out.

Do not commit or push unless the user asks.

## Guardrails / anti-patterns

- Do **not** edit anything before approval; deep-change items need a second yes.
- Do **not** invent findings to justify a change — a clean session yields few or none.
- Do **not** cause drastic evolution; respect the level ceiling.
- Do **not** make skills longer "to be safe" — prefer cutting or moving detail
  to a reference file. Never drop a real instruction while condensing.
- Do **not** let autonomous analysis become noise — apply the relevance bar
  (real effect on time, tokens, or correctness).

## Reference files

- `reference/process-analysis.md` — the six-lens first-principles engine,
  severity→level mapping, and relevance bar. Read in Step 2.
- `reference/evaluation-rubric.md` — scoring dimensions and token heuristics.
  Read in Step 5.
- `reference/length-and-structure.md` — the ~200-line mechanism, how to split
  into references, navigation convention, light-condensing rules. Read in Step 5.
- `reference/skill-template.md` — structure/frontmatter for a new skill. Read in
  Step 4 when proposing one.
