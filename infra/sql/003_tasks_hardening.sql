ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS locked_at TIMESTAMP;

ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS locked_by TEXT;

CREATE INDEX IF NOT EXISTS idx_tasks_processing_timeout
ON tasks (status, locked_at);
