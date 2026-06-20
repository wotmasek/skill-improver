Part of the **skill-improver** skill — read in Step 0 (backward review) and
Step 7 (logging), and whenever you log an error. This is the full mechanism; the
main `SKILL.md` only summarizes it.

# Closed-Loop Verification & Ledger

skill-improver must not change skills on belief alone. Every change ("mutation")
is logged with its **expected effect**, and on later runs the skill checks
whether that effect held — confirming, or rolling back what didn't work. This
closes the loop and gives the skill memory across sessions.

## Storage

A small SQLite store, accessed only through the helper script
`scripts/ledger.py` (Python 3 stdlib, no dependencies).

- Live db — `data/ledger.db` — **gitignored**, treated as a rebuildable cache.
- Canonical store — `data/ledger.sql` — a **committed** text dump, so history is
  diffable and reviewable in PRs and survives ephemeral web sessions.
- The helper restores the db from the dump when it's missing and re-dumps after
  every write. You never touch the files directly — just call the helper.

`git` remains the source of truth for *content* and *rollback*: each mutation is
a commit, so the ledger stores only metadata + verdicts keyed by `commit_sha`,
never full diffs.

## Schema

`mutations` — one row per applied change:
`id, created_at, commit_sha, target, kind, level, rationale, expected_effect,
source, status, verified_at, verdict_note`
- `status`: `pending | confirmed_good | ineffective | harmful | rolled_back`
- `kind`: trigger / clarity / missing-step / example / efficiency / new-skill / adjacent
- `source`: `feedback | autonomous`

`errors` — one row per problem reported or observed:
`id, created_at, description, cause, target, severity, source, related_mutation_id`
- `source`: `user_report | observed`
- `related_mutation_id`: set when the error is a recurrence of, or a regression
  from, a known mutation.

## Helper commands

```
python3 scripts/ledger.py init
python3 scripts/ledger.py log-mutation --commit <sha> --target <skill> \
    --kind <kind> --level <L1|L2|L3> --rationale "<finding>" \
    --expected "<expected effect>" --source <feedback|autonomous>
python3 scripts/ledger.py log-error --description "<what>" --cause "<why>" \
    --target <skill> --severity <good|mediocre|bad> \
    --source <user_report|observed> [--related <mutation_id>]
python3 scripts/ledger.py pending     # mutations awaiting a verdict + evidence
python3 scripts/ledger.py verdict --id <id> --status <status> --note "<why>"
python3 scripts/ledger.py report      # full summary + rollback candidates
```

`pending` returns, for each unverified mutation, the errors that postdate it on
the same target (`subsequent_errors`). That is the structured evidence — the
**judgment is yours**, made by reasoning over the rows, not by the query.

## Assigning a verdict (Step 0)

For each `pending` mutation past its evidence window, decide:

- **`ineffective`** — the original problem recurs (a later error matches the
  mutation's `rationale`/`expected_effect`). The change didn't deliver.
- **`harmful`** — new problems appear in the area the mutation touched (a
  regression). → propose rollback.
- **`confirmed_good`** — the evidence window elapsed with no related errors and,
  where checkable, the expected effect held.
- **stay `pending`** — not enough has happened yet. Never judge prematurely
  (consistent with the rule-of-three / recurrence principle).

**Evidence window (default, adjustable):** treat a mutation as judgeable once
there has been at least one subsequent skill-improver run touching that target,
**or** ~7 days have passed. Until then, leave it `pending`.

Record every decision with `verdict` (include a short `--note` with the
evidence) so the reasoning is auditable.

## Rollback (proposed, never automatic)

For a `harmful` mutation:

1. Show the evidence (the mutation row + the errors that condemn it).
2. Propose `git revert <commit_sha>`. If a clean revert is blocked by later
   commits on the same lines, propose a targeted corrective edit instead.
3. After the user approves and the revert/edit is committed, set
   `verdict --status rolled_back --note "<reverted in <sha>; reason>"`.

Rollback follows the skill's **propose, don't impose** rule — present it, get the
yes, then act.

## Logging errors — three entry points

1. **At a skill-improver run (Step 1):** log problems surfaced by the user's
   feedback (`--source user_report`) and ones you observed (`--source observed`).
2. **On demand:** the `/skill-log-error` command captures a problem the moment it
   happens, without waiting for a full retrospective.
3. **Best-effort hook:** a `PostToolUse` hook may append an `observed` error when
   a test/build command fails. It catches only mechanical failures — semantic or
   quality problems still need a human. Keep it conservative; drop it if noisy.

## Logging mutations (Step 7)

After approved changes are committed, for **each** change call `log-mutation`
with its `commit_sha`, the `expected_effect` you already stated in the proposal,
the `target`, `kind`, `level`, and `source`. Then commit the updated
`data/ledger.sql` alongside.
