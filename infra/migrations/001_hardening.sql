ALTER TABLE processing_queue
ADD COLUMN IF NOT EXISTS attempts INT DEFAULT 0;

CREATE TABLE IF NOT EXISTS processing_dlq (
    id SERIAL PRIMARY KEY,
    task_id INT,
    task_type TEXT,
    payload JSONB,
    error TEXT,
    failed_at TIMESTAMP DEFAULT NOW()
);
