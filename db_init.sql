CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_uuid UUID DEFAULT gen_random_uuid(),

    type TEXT NOT NULL,
    payload JSONB NOT NULL,

    status TEXT DEFAULT 'pending', -- pending | processing | done | failed

    priority INT DEFAULT 5,

    retries INT DEFAULT 0,
    max_retries INT DEFAULT 3,

    run_after TIMESTAMP DEFAULT NOW(),

    locked_at TIMESTAMP,
    locked_by TEXT,

    last_error TEXT,

    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_priority
ON tasks(status, priority DESC);

CREATE INDEX IF NOT EXISTS idx_tasks_run_after
ON tasks(run_after);
