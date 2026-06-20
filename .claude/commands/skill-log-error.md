---
description: Log a problem/error into the skill-improver ledger right now, without running a full retrospective.
---

Quickly record a problem in the skill-improver verification ledger so a later
`/skill-improver` run can judge whether a past change caused it.

User's note about the problem: $ARGUMENTS

Do this:

1. From the note (and the recent conversation), determine:
   - `description` — what went wrong, in one line.
   - `cause` — the likely root cause, if known (else leave empty).
   - `target` — the skill or area implicated, if identifiable (else omit).
   - `severity` — `good` / `mediocre` / `bad`.
   - If this looks like a recurrence of, or regression from, a known change,
     find its mutation id via `python3 .claude/skills/skill-improver/scripts/ledger.py report`
     and pass `--related <id>`.

2. Append it:

   ```
   python3 .claude/skills/skill-improver/scripts/ledger.py log-error \
       --description "<...>" --cause "<...>" --target "<...>" \
       --severity "<...>" --source user_report [--related <id>]
   ```

3. Commit the updated `data/ledger.sql` (do not commit `ledger.db`). Confirm to
   the user what was logged in one line. Do not start a retrospective or change
   any skill — that is `/skill-improver`'s job.
