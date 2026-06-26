CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    payload JSONB NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_created
ON tasks(status, created_at);
