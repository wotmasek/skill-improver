Part of the **skill-improver** skill — read in Step 2 to run the autonomous,
first-principles analysis of the process (independent of user feedback).

# First-Principles Process Analysis

Goal: relentlessly find how the process could have produced a *higher-quality
final output* — and, without ever sacrificing that quality, in fewer steps /
tokens. Quality is the primary target; step/token savings are secondary and only
count when the final result is as good or better. Be ambitious about *finding*
improvements and conservative about *applying* them (the level in Step 3 caps how
far you go).

Feedback is the priority signal, but this engine must always run and stand on
its own. The strongest sessions to analyze are the ones the user thought were
"fine" — that is where an unnoticed quality ceiling, or waste that could be cut
without touching quality, tends to hide.

## The six lenses

Run the session through each, in order. The order matters: deleting beats
simplifying, simplifying beats automating something that shouldn't exist.

1. **Question the requirement.** Was each step actually needed for the goal? Did
   a skill make us do work that didn't serve the outcome? Challenge every
   "required" assumption — name who/what it came from.
2. **Delete.** What step, instruction, file read, search, or tool call could be
   removed entirely with no loss? The best optimization is a deleted step. If
   you later have to add something back, you deleted too little.
3. **Simplify / merge.** What remained — can it be shorter, combined, or
   expressed once instead of three ways? Collapse redundant instructions.
4. **Reorder / accelerate.** What was done out of order and caused rework? What
   narrowing/gating should happen earlier so later steps do less? What ran
   sequentially that could have been one batched action?
5. **Automate / systematize.** What manual or repeated thing should become a
   codified step, a slash command, or a hook so it never has to be re-decided?
6. **Cache / reuse.** What was re-read, re-searched, or re-derived that should
   have been captured once and reused? Encode "gather X once, here" into the skill.

**Quality guard for every lens.** Deleting, simplifying, or reordering is a win
only if the *final* output stays as good or better. If removing a step would
lower the quality of the result, that is degradation, not optimization — keep
the step. Lenses 1–4 trim how the result is *reached*, never what it *is*.

## The relevance bar

Only surface a finding if it plausibly improves **final output quality or
correctness**, or cuts **time/tokens without costing quality**, in a way that
would recur. Drop:

- one-off hiccups unlikely to repeat,
- stylistic preferences with no measurable effect,
- "nice to have" additions that cost tokens on every future run for rare benefit.

If you cannot name the expected effect ("produces a more complete/correct
result", "stops the skill firing on lookalikes", "saves a full re-read of the
file"), it is not a finding yet.

## Severity → modification level

Your analysis also calibrates the Step 3 level. Judge the *process*, blending
the user's feedback tone with what the timeline shows:

| Severity | Signals | Level |
|----------|---------|-------|
| Good | smooth path, minor nits, no real rework | **L1 Surgical** |
| Mediocre | some detours/retries, fixable friction | **L2 Structural** (default) |
| Bad | major wasted effort, repeated corrections, wrong outcomes | **L3 Deep** |

Feedback severity and observed severity can differ — if the user is unhappy,
respect that even if the timeline looks clean; if the user is content but the
timeline shows real waste, surface it as autonomous findings but stay at the
lower level unless they agree to go deeper.

## Output

A ranked list of autonomous findings. For each: **lens** it came from,
**evidence** (the concrete moment), **proposed change**, **level required**, and
**expected effect**. These feed Step 6 alongside the priority feedback findings.
