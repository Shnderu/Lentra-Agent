CREATE TABLE IF NOT EXISTS workflows (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS workflow_nodes (
    id SERIAL PRIMARY KEY,
    workflow_id INT REFERENCES workflows(id),
    node_key TEXT,
    task_type TEXT,
    config JSONB,
    depends_on TEXT[]
);

CREATE TABLE IF NOT EXISTS workflow_runs (
    id SERIAL PRIMARY KEY,
    workflow_id INT,
    status TEXT DEFAULT 'running',
    trace_id TEXT,
    started_at TIMESTAMP DEFAULT NOW(),
    finished_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS workflow_tasks (
    id SERIAL PRIMARY KEY,
    run_id INT,
    node_key TEXT,
    status TEXT DEFAULT 'pending',
    payload JSONB,
    attempts INT DEFAULT 0
);
