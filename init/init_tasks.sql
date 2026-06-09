CREATE TABLE IF NOT EXISTS public.tasks (
    id SERIAL PRIMARY KEY,
    task_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    priority INT DEFAULT 100,
    status TEXT DEFAULT 'pending',
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    locked_at TIMESTAMP,
    lease_until TIMESTAMP,
    worker_id TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_tasks_status_priority
ON public.tasks(status, priority DESC, id);
