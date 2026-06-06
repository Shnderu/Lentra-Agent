CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'new',

    priority INT NOT NULL DEFAULT 5,
    retries INT NOT NULL DEFAULT 0,

    last_error TEXT,

    run_after TIMESTAMP,
    locked_at TIMESTAMP,
    locked_by TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_priority
ON tasks(status, priority DESC);

CREATE INDEX IF NOT EXISTS idx_tasks_run_after
ON tasks(run_after);
