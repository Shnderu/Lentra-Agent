-- =========================
-- FLYRUM CORE SCHEMA v3.6.1
-- =========================

-- TASK QUEUE
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT DEFAULT 'pending',
    priority INT DEFAULT 5,
    retries INT DEFAULT 0,
    run_after TIMESTAMP DEFAULT NOW(),
    locked_at TIMESTAMP,
    locked_by TEXT,
    last_error TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
CREATE INDEX IF NOT EXISTS idx_tasks_run_after ON tasks(run_after);

-- ROUTES (минимальная схема из кода)
CREATE TABLE IF NOT EXISTS routes (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    route TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_routes_user_id ON routes(user_id);
