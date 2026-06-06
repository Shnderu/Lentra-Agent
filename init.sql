CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT DEFAULT 'new',
    priority INT DEFAULT 0,
    retries INT DEFAULT 0,
    last_error TEXT,
    run_after TIMESTAMP,
    locked_at TIMESTAMP,
    locked_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);

CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    user_id BIGINT,
    route TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
