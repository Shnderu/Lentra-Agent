DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,

    task_type TEXT NOT NULL,
    payload JSONB NOT NULL,

    status TEXT NOT NULL DEFAULT 'pending',

    priority INT DEFAULT 5,

    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,

    locked_at TIMESTAMP NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_status_priority
    ON tasks(status, priority DESC);

CREATE INDEX idx_tasks_locked_at
    ON tasks(locked_at);

CREATE INDEX idx_tasks_attempts
    ON tasks(attempts);
