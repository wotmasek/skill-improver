#!/usr/bin/env python3
"""Ledger helper for skill-improver's closed-loop verification.

Stores a log of mutations (changes the skill applied) and errors (problems the
user reported or that were observed), so later runs can judge whether each
mutation was good and roll back the bad ones.

Storage model: the live SQLite db (data/ledger.db) is gitignored; the canonical,
committed artifact is a text SQL dump (data/ledger.sql) so git holds a diffable,
reviewable history. Read commands lazily restore the db from the dump if missing;
write commands re-dump afterward. The skill just calls this script — the
dump/restore is internal.

Python 3 stdlib only.
"""

import argparse
import json
import os
import sqlite3
import sys
from datetime import datetime, timezone

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
DB_PATH = os.path.join(DATA_DIR, "ledger.db")
SQL_PATH = os.path.join(DATA_DIR, "ledger.sql")

SCHEMA = """
CREATE TABLE IF NOT EXISTS mutations (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at      TEXT NOT NULL,
    commit_sha      TEXT,
    target          TEXT NOT NULL,
    kind            TEXT,
    level           TEXT,
    rationale       TEXT,
    expected_effect TEXT,
    source          TEXT,
    status          TEXT NOT NULL DEFAULT 'pending',
    verified_at     TEXT,
    verdict_note    TEXT
);

CREATE TABLE IF NOT EXISTS errors (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at          TEXT NOT NULL,
    description         TEXT NOT NULL,
    cause               TEXT,
    target              TEXT,
    severity            TEXT,
    source              TEXT,
    related_mutation_id INTEGER REFERENCES mutations(id)
);
"""

VALID_STATUS = {"pending", "confirmed_good", "ineffective", "harmful", "rolled_back"}


def now() -> str:
    # Microsecond precision so a mutation and an error logged in the same second
    # still order correctly (the pending query uses created_at > mutation time).
    return datetime.now(timezone.utc).isoformat(timespec="microseconds")


def ensure_db() -> sqlite3.Connection:
    """Open the db, restoring from the committed SQL dump if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    fresh = not os.path.exists(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    if fresh and os.path.exists(SQL_PATH):
        with open(SQL_PATH, "r", encoding="utf-8") as fh:
            conn.executescript(fh.read())
    conn.executescript(SCHEMA)  # idempotent; guarantees tables exist
    conn.commit()
    return conn


def dump(conn: sqlite3.Connection) -> None:
    """Write the canonical text dump that git tracks."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(SQL_PATH, "w", encoding="utf-8") as fh:
        fh.write("-- skill-improver ledger. Canonical committed store.\n")
        fh.write("-- Live ledger.db is rebuilt from this file and is gitignored.\n")
        for line in conn.iterdump():
            fh.write(f"{line}\n")


def cmd_init(args, conn):
    dump(conn)
    print(f"Initialized ledger at {os.path.relpath(DB_PATH)} (dump: {os.path.relpath(SQL_PATH)})")


def cmd_log_mutation(args, conn):
    cur = conn.execute(
        """INSERT INTO mutations
           (created_at, commit_sha, target, kind, level, rationale,
            expected_effect, source, status)
           VALUES (?,?,?,?,?,?,?,?, 'pending')""",
        (now(), args.commit, args.target, args.kind, args.level,
         args.rationale, args.expected, args.source),
    )
    conn.commit()
    dump(conn)
    print(json.dumps({"mutation_id": cur.lastrowid}))


def cmd_log_error(args, conn):
    cur = conn.execute(
        """INSERT INTO errors
           (created_at, description, cause, target, severity, source,
            related_mutation_id)
           VALUES (?,?,?,?,?,?,?)""",
        (now(), args.description, args.cause, args.target, args.severity,
         args.source, args.related),
    )
    conn.commit()
    dump(conn)
    print(json.dumps({"error_id": cur.lastrowid}))


def cmd_pending(args, conn):
    """List pending mutations with the errors that postdate them on the same
    target — the structured evidence the skill reasons over to assign a verdict."""
    out = []
    for m in conn.execute(
        "SELECT * FROM mutations WHERE status='pending' ORDER BY created_at"
    ).fetchall():
        ev = conn.execute(
            """SELECT id, created_at, description, cause, severity, source
               FROM errors
               WHERE created_at > ?
                 AND (target = ? OR target IS NULL)
               ORDER BY created_at""",
            (m["created_at"], m["target"]),
        ).fetchall()
        row = dict(m)
        row["subsequent_errors"] = [dict(e) for e in ev]
        out.append(row)
    print(json.dumps(out, indent=2))


def cmd_verdict(args, conn):
    if args.status not in VALID_STATUS:
        sys.exit(f"invalid status '{args.status}'; choose from {sorted(VALID_STATUS)}")
    n = conn.execute(
        "UPDATE mutations SET status=?, verified_at=?, verdict_note=? WHERE id=?",
        (args.status, now(), args.note, args.id),
    ).rowcount
    conn.commit()
    dump(conn)
    if not n:
        sys.exit(f"no mutation with id {args.id}")
    print(json.dumps({"mutation_id": args.id, "status": args.status}))


def cmd_report(args, conn):
    muts = [dict(r) for r in conn.execute(
        "SELECT * FROM mutations ORDER BY created_at DESC"
    ).fetchall()]
    errs = [dict(r) for r in conn.execute(
        "SELECT * FROM errors ORDER BY created_at DESC"
    ).fetchall()]
    counts = {}
    for m in muts:
        counts[m["status"]] = counts.get(m["status"], 0) + 1
    print(json.dumps({
        "status_counts": counts,
        "rollback_candidates": [m for m in muts if m["status"] == "harmful"],
        "mutations": muts,
        "errors": errs,
    }, indent=2))


def build_parser():
    p = argparse.ArgumentParser(description="skill-improver ledger")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init").set_defaults(func=cmd_init)

    m = sub.add_parser("log-mutation")
    m.add_argument("--commit")
    m.add_argument("--target", required=True)
    m.add_argument("--kind")
    m.add_argument("--level")
    m.add_argument("--rationale")
    m.add_argument("--expected")
    m.add_argument("--source", default="autonomous")
    m.set_defaults(func=cmd_log_mutation)

    e = sub.add_parser("log-error")
    e.add_argument("--description", required=True)
    e.add_argument("--cause")
    e.add_argument("--target")
    e.add_argument("--severity")
    e.add_argument("--source", default="user_report")
    e.add_argument("--related", type=int)
    e.set_defaults(func=cmd_log_error)

    sub.add_parser("pending").set_defaults(func=cmd_pending)

    v = sub.add_parser("verdict")
    v.add_argument("--id", type=int, required=True)
    v.add_argument("--status", required=True)
    v.add_argument("--note")
    v.set_defaults(func=cmd_verdict)

    sub.add_parser("report").set_defaults(func=cmd_report)
    return p


def main():
    args = build_parser().parse_args()
    conn = ensure_db()
    try:
        args.func(args, conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()
