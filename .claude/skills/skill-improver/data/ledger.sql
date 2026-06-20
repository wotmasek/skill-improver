-- skill-improver ledger. Canonical committed store.
-- Live ledger.db is rebuilt from this file and is gitignored.
BEGIN TRANSACTION;
CREATE TABLE errors (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at          TEXT NOT NULL,
    description         TEXT NOT NULL,
    cause               TEXT,
    target              TEXT,
    severity            TEXT,
    source              TEXT,
    related_mutation_id INTEGER REFERENCES mutations(id)
);
CREATE TABLE mutations (
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
DELETE FROM "sqlite_sequence";
COMMIT;
