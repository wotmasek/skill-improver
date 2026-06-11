Part of the **skill-improver** skill — read in Step 2 to run the autonomous,
first-principles analysis of the process (independent of user feedback).

# First-Principles Process Analysis

Goal: relentlessly find how the process could have produced a *better* output in
*fewer* tokens / steps — and encode that into the skills. Be ambitious about
*finding* optimizations and conservative about *applying* them (the level in
Step 3 caps how far you go).

Feedback is the priority signal, but this engine must always run and stand on
its own. The strongest sessions to analyze are the ones the user thought were
"fine" — that is where unnoticed waste hides.

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

## The relevance bar

Only surface a finding if it plausibly changes **time, tokens, or correctness**
in a way that would recur. Drop:

- one-off hiccups unlikely to repeat,
- stylistic preferences with no measurable effect,
- "nice to have" additions that cost tokens on every future run for rare benefit.

If you cannot name the expected effect ("saves a full re-read of the file",
"stops the skill firing on lookalikes", "removes ~30 lines paid every load"),
it is not a finding yet.

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
