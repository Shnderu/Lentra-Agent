CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,
    priority INT DEFAULT 1,
    status TEXT DEFAULT 'pending',
    retries INT DEFAULT 0,
    max_retries INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_priority
ON tasks(status, priority DESC);
