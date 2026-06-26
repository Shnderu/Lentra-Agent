CREATE TABLE IF NOT EXISTS task_queue (
    id UUID PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,

    status TEXT NOT NULL DEFAULT 'pending',

    attempts INT NOT NULL DEFAULT 0,
    max_attempts INT NOT NULL DEFAULT 5,

    run_after TIMESTAMP NOT NULL DEFAULT now(),

    locked_at TIMESTAMP NULL,
    locked_by TEXT NULL,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_queue_status_run
ON task_queue(status, run_after);

CREATE INDEX IF NOT EXISTS idx_queue_locked
ON task_queue(locked_at);
