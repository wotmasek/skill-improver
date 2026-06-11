Part of the **skill-improver** skill — read in Step 5 to score a target skill.

# Skill Evaluation Rubric

Use this when scoring a target skill. For each dimension, decide: PASS (leave
it), WEAK (propose an improvement), or MISSING (add it). Always attach the
finding to something that actually happened in the session.

> File-length and structure (the ~200-line split, navigation, light condensing)
> is handled by `reference/length-and-structure.md`, not here. This rubric scores
> *quality*; that file handles the *mechanism*.

## 1. Trigger / description accuracy

The `description` in the frontmatter is the *only* thing the model sees when
deciding whether to load the skill. This is the #1 reason skills fail — they
don't fire, or they fire at the wrong time.

Check:
- Does it name the concrete situations, verbs, and user phrasings that should
  activate it? ("when the user asks to…", "when X fails", slash-command name)
- Does it include negative scope so it does **not** fire on lookalikes?
- In this session, did the skill fire when it should have? If it didn't, the
  description is the first suspect.

Good descriptions are specific about *when*, not *what*. "Formats dates" is bad;
"Use when parsing or formatting dates/timezones; do NOT use for durations" is good.

## 2. Instruction clarity

- Are steps in the order they must actually be done?
- Is each step a concrete action, not a vague intention?
- Are there hidden prerequisites the skill assumes but never states?
- Did the session reveal a step that was ambiguous and led to a wrong guess?

## 3. Missing steps & anti-patterns

- Add any step whose absence caused rework this session.
- Add an explicit "do NOT do X" for each mistake that actually occurred. Naming
  the failure mode is cheaper than letting it recur.
- Prefer one sharp warning over a paragraph of caveats.

## 4. Examples & counter-examples

- One concrete "use when…" example beats three sentences of description.
- Add a counter-example ("do NOT use when…") if the skill fired wrongly, or
  could plausibly be confused with a neighbor skill.
- Examples should reflect real situations from the session when possible.

## 5. Token efficiency vs. output quality

The goal is a *better* output for *fewer* tokens. Both matter — never trade away
correctness for brevity.

Look for waste the session exposed:
- **Re-reads / redundant tool calls.** If the work re-read a file or re-ran a
  search the skill should have prevented, fix the instruction so it gathers the
  right thing once.
- **Bloated SKILL.md.** Detail that's only needed sometimes belongs in a
  `reference/` file (progressive disclosure) so it isn't paid for on every load.
- **Oversized outputs.** If a step pulls huge tool output into context, scope it
  (line ranges, filters, counts instead of dumps).
- **Repetition.** Instructions that restate the same rule three ways — collapse them.
- **Premature breadth.** Steps that fan out before narrowing — add a "narrow first"
  instruction.

For every proposed *addition*, ask: does this earn its tokens on every future
run? If it only helps rarely, move it to a reference file or cut it.

## Output of the evaluation

A ranked list of findings. For each: dimension, what happened (evidence),
proposed change (diff), expected effect. Priority findings from the user's own
feedback (Step 1) always rank first.
