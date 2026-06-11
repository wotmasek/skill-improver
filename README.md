# skill-improver

A Claude Code skill that runs a retrospective on the work just done and turns
the lessons into concrete improvements to your existing skills — or a draft of a
new one when it spots a gap.

## What it does

Invoke it manually with `/skill-improver` after finishing a task. It will:

1. **Ask for your feedback first** and treat it as the highest-priority signal.
2. **Run two retrospective engines** — your feedback *and* its own
   first-principles process analysis (six lenses: question the requirement →
   delete → simplify → reorder → automate → cache), with a relevance bar so it
   surfaces only changes that affect time, tokens, or correctness.
3. **Pick a modification level from how it actually went** — went well → L1
   surgical, mediocre → L2 structural (default), went badly → L3 deep. The level
   caps how far a single run may go, so improvements stay incremental, never
   drastic. Changing what a skill fundamentally *does* needs a separate explicit
   approval.
4. **Map findings to skills** in `.claude/skills/` (or a skill you point at) —
   and, when useful, to adjacent mechanisms (a hook, command, or settings change).
5. **Evaluate** each skill on trigger accuracy, instruction clarity, missing
   steps/anti-patterns, examples, and token efficiency, and **keep files lean**:
   ~200-line soft threshold, split into navigable references, *light* condensing
   that never drops an instruction.
6. **Propose changes as a diff** and wait for your approval before editing
   anything. When it finds a recurring pattern with no skill, it drafts a new one.

It never edits a skill silently — you approve first.

## Layout

```
.claude/skills/skill-improver/
├── SKILL.md                          # workflow (loaded on trigger)
└── reference/
    ├── process-analysis.md           # six-lens engine + severity→level mapping
    ├── evaluation-rubric.md          # scoring dimensions + token heuristics
    ├── length-and-structure.md       # ~200-line split, navigation, condensing
    └── skill-template.md             # structure for drafting a new skill
```

## Install

Project-scoped already (lives in `.claude/skills/`). To use it globally across
all projects, copy the `skill-improver` directory into `~/.claude/skills/`.
