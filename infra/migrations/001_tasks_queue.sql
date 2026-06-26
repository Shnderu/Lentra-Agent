CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY,
    flow JSONB NOT NULL,

    status TEXT NOT NULL DEFAULT 'pending',

    attempts INT NOT NULL DEFAULT 0,
    max_attempts INT NOT NULL DEFAULT 5,

    locked_at TIMESTAMP NULL,
    locked_by TEXT NULL,

    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
