# skill-improver

A Claude Code skill that runs a retrospective on the work just done and turns
the lessons into concrete improvements to your existing skills — or a draft of a
new one when it spots a gap.

## What it does

Invoke it manually with `/skill-improver` after finishing a task. It will:

1. **Ask for your feedback first** and treat it as the highest-priority signal.
2. **Reconstruct what happened** this session — detours, rework, wasted tokens,
   places it had to be corrected.
3. **Map findings to skills** in `.claude/skills/` (or a skill you point at).
4. **Evaluate** each skill on trigger accuracy, instruction clarity, missing
   steps/anti-patterns, examples, and token efficiency vs. output quality.
5. **Propose changes as a diff** and wait for your approval before editing
   anything. When it finds a recurring pattern with no skill, it drafts a new one.

It never edits a skill silently — you approve first.

## Layout

```
.claude/skills/skill-improver/
├── SKILL.md                          # workflow (loaded on trigger)
└── reference/
    ├── evaluation-rubric.md          # scoring dimensions + token heuristics
    └── skill-template.md             # structure for drafting a new skill
```

## Install

Project-scoped already (lives in `.claude/skills/`). To use it globally across
all projects, copy the `skill-improver` directory into `~/.claude/skills/`.
