-- v3.6 PRODUCTION CORE SCHEMA

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT DEFAULT 'pending',
    priority INT DEFAULT 5,
    retries INT DEFAULT 3,
    run_after TIMESTAMP DEFAULT NOW(),
    locked_at TIMESTAMP,
    locked_by TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status
ON tasks(status);

CREATE INDEX IF NOT EXISTS idx_tasks_run_after
ON tasks(run_after);

CREATE INDEX IF NOT EXISTS idx_tasks_priority
ON tasks(priority);

-- Dead letter queue (failed tasks permanently)
CREATE TABLE IF NOT EXISTS dead_letter (
    id SERIAL PRIMARY KEY,
    task_id INT,
    payload JSONB,
    reason TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
