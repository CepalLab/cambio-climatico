PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS documents (
    handle TEXT PRIMARY KEY,
    corpus_order INTEGER NOT NULL UNIQUE,
    title TEXT NOT NULL,
    publication_year TEXT,
    source_csv TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN (
        'pending', 'queued', 'in_progress', 'processed',
        'error_retryable', 'error', 'review', 'approved'
    )),
    current_stage TEXT NOT NULL DEFAULT 'pending' CHECK (current_stage IN (
        'pending', 'acquisition', 'extraction', 'enrichment',
        'validation', 'review', 'completed'
    )),
    retry_count INTEGER NOT NULL DEFAULT 0,
    max_retries INTEGER NOT NULL DEFAULT 3,
    active_batch_id INTEGER REFERENCES batches(id),
    result_path TEXT,
    source_pdf_path TEXT,
    source_text_path TEXT,
    model TEXT,
    prompt_version TEXT,
    freeze_version TEXT,
    last_error TEXT,
    lease_expires_at TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS batches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE,
    name TEXT,
    status TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'completed', 'cancelled')),
    requested_size INTEGER NOT NULL,
    freeze_version TEXT NOT NULL,
    manifest_path TEXT,
    created_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE TABLE IF NOT EXISTS batch_documents (
    batch_id INTEGER NOT NULL REFERENCES batches(id),
    handle TEXT NOT NULL REFERENCES documents(handle),
    position INTEGER NOT NULL,
    assigned_at TEXT NOT NULL,
    PRIMARY KEY (batch_id, handle),
    UNIQUE (batch_id, position)
);

CREATE TABLE IF NOT EXISTS attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT NOT NULL REFERENCES documents(handle),
    batch_id INTEGER REFERENCES batches(id),
    attempt_no INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('running', 'failed', 'interrupted', 'completed')),
    model TEXT,
    prompt_version TEXT,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cost_usd REAL,
    error_message TEXT,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    UNIQUE (handle, attempt_no)
);

CREATE TABLE IF NOT EXISTS checkpoints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT NOT NULL REFERENCES documents(handle),
    batch_id INTEGER REFERENCES batches(id),
    attempt_no INTEGER NOT NULL,
    stage TEXT NOT NULL CHECK (stage IN (
        'acquisition', 'extraction', 'enrichment', 'validation', 'review'
    )),
    artifact_path TEXT,
    metadata_json TEXT,
    created_at TEXT NOT NULL,
    UNIQUE (handle, attempt_no, stage)
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    handle TEXT REFERENCES documents(handle),
    batch_id INTEGER REFERENCES batches(id),
    event_type TEXT NOT NULL,
    from_status TEXT,
    to_status TEXT,
    detail TEXT,
    created_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_documents_status_order
    ON documents(status, corpus_order);
CREATE INDEX IF NOT EXISTS idx_documents_batch_status
    ON documents(active_batch_id, status);
CREATE INDEX IF NOT EXISTS idx_attempts_handle
    ON attempts(handle, attempt_no DESC);
CREATE INDEX IF NOT EXISTS idx_events_handle
    ON events(handle, created_at DESC);
