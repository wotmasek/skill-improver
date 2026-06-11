Part of the **skill-improver** skill — read in Step 5 to keep skill files lean
and navigable as you propose changes.

# Length & Structure Mechanism

Every line in a `SKILL.md` is a token cost paid on **every** invocation. Keep
the main file lean; push depth into `reference/` files read only on demand
(progressive disclosure).

## The ~200-line threshold (soft)

- ~200 lines is a **soft trigger** for any `SKILL.md`, not a hard cap. Split
  earlier when content is optional, rarely needed, or only relevant in one
  branch of the workflow.
- A skill is "overgrown" when any of these hold:
  - `SKILL.md` is past ~200 lines,
  - one section dominates the file,
  - reference files duplicate material already in the main file,
  - detail is present that most invocations never use.
- When triggered, **propose** (don't silently apply) extracting the optional or
  deep content into `reference/<topic>.md`, leaving the main file with the
  always-needed workflow plus pointers.

## What stays in SKILL.md vs. moves to reference

- **Stays:** the trigger description, the core ordered workflow, control flow
  needed every run (e.g. level rules), short guardrails, the reference index.
- **Moves:** question banks, rubrics, templates, long examples, edge-case
  detail, anything read only in one step or one branch.

## Navigation convention (so references are easy to move between)

- `SKILL.md` keeps a **Reference files** index: each entry = file + one-line
  purpose + *when to read it* (which step/condition).
- Each reference file opens with a one-line **backlink**: "Part of the **X**
  skill — read in Step N when …".
- Use stable, descriptive section headers so a step can point at a specific
  section. Keep one topic per reference file.

## Light condensing (emphasis on *light*)

When a skill has grown bloated, condense — but conservatively:

- Remove only **redundancy**: repeated rules, the same point made three ways,
  filler prose, dead caveats.
- **Never drop** an instruction, a warning, a step, or an example that carries
  unique information. When unsure whether something is redundant, **keep it**.
- Condensing is **behavior-preserving** — it changes wording/structure, not what
  the skill does, so it lives within L2+ and never needs the deep-change gate.
- Prefer one sharp sentence over a paragraph; prefer a list over repetition; do
  not compress to the point of ambiguity. Brevity that loses clarity is a
  regression, not an optimization.

## Output

For each overgrown target: a proposed split (which content → which new reference
file), updated navigation, and the condensed wording — presented as a diff in
Step 6 like any other change.
