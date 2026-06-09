CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,

    status TEXT DEFAULT 'queued',
    attempts INT DEFAULT 0,

    run_after TIMESTAMP DEFAULT NOW(),

    locked_at TIMESTAMP,
    locked_by TEXT,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_run_after ON tasks(run_after);
