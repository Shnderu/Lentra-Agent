CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    type TEXT,
    payload JSONB,
    status TEXT DEFAULT 'new',
    priority INT DEFAULT 0,
    retries INT DEFAULT 0,
    max_retries INT DEFAULT 3
);
