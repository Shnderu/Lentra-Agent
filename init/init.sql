CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_type TEXT,
    payload JSONB,
    priority INT DEFAULT 0,

    status TEXT DEFAULT 'pending',
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,

    locked_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),

    worker_id TEXT,
    retry_at TIMESTAMP
);
