CREATE TABLE IF NOT EXISTS tasks_dlq (
    id SERIAL PRIMARY KEY,
    original_task_id INT,
    task_type TEXT,
    payload JSONB,
    error TEXT,
    failed_at TIMESTAMP DEFAULT NOW()
);
