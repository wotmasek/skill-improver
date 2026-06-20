# skill-improver

A Claude Code skill that runs a retrospective on the work just done and turns
the lessons into concrete improvements to your existing skills — or a draft of a
new one when it spots a gap.

## What it does

Invoke it manually with `/skill-improver` after finishing a task. It will:

0. **Verify past changes first (closed loop).** Before anything new, it reviews
   the changes it made earlier against what happened since — confirming the ones
   that worked and proposing a rollback (`git revert`) for any that caused
   problems. It remembers across sessions via a small committed ledger.
1. **Ask for your feedback first** and treat it as the highest-priority signal.
2. **Run two retrospective engines** — your feedback *and* its own
   first-principles process analysis (six lenses: question the requirement →
   delete → simplify → reorder → automate → cache), with a relevance bar so it
   surfaces only changes that raise final quality, or cut steps/tokens without
   costing quality. **Quality comes first, cost second — it never trades final
   quality for fewer tokens unless you explicitly ask for that tradeoff.**
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
├── reference/
│   ├── verification-and-ledger.md    # closed-loop store, verdicts, rollback
│   ├── process-analysis.md           # six-lens engine + severity→level mapping
│   ├── evaluation-rubric.md          # scoring dimensions + token heuristics
│   ├── length-and-structure.md       # ~200-line split, navigation, condensing
│   └── skill-template.md             # structure for drafting a new skill
├── scripts/
│   ├── ledger.py                     # SQLite ledger CLI (stdlib only)
│   └── hook_log_failure.py           # best-effort PostToolUse failure logger
└── data/
    └── ledger.sql                    # committed text store (ledger.db gitignored)
.claude/commands/skill-log-error.md   # /skill-log-error quick logging
```

## Closed-loop verification

Each change skill-improver applies is logged (with its expected effect, keyed by
git commit) into a small SQLite ledger. Problems get logged too — at a run, via
`/skill-log-error`, or by a best-effort hook on failed test/build commands. On
later runs the skill judges each past change and proposes reverting the harmful
ones. The live `ledger.db` is rebuilt from the committed, diffable `ledger.sql`,
so the history survives ephemeral sessions and is reviewable in PRs.

## Install

Project-scoped already (lives in `.claude/`). To use it globally across all
projects, copy the `skill-improver` directory into `~/.claude/skills/` (and the
command into `~/.claude/commands/`). Requires Python 3 (standard library only).
