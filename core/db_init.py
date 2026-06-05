from core.db.connection import get_conn


def run_migrations():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS routes (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            route TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id SERIAL PRIMARY KEY,
            user_id BIGINT,
            payload JSONB,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            task_type TEXT NOT NULL,
            payload JSONB NOT NULL,
            status TEXT DEFAULT 'pending',
            priority INT DEFAULT 5,
            retries INT DEFAULT 3,
            run_after TIMESTAMP DEFAULT NOW(),
            locked_at TIMESTAMP NULL,
            locked_by TEXT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_status_run
        ON tasks(status, run_after)
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_priority
        ON tasks(priority)
    """)

    conn.commit()
    cur.close()
    conn.close()


def init_db():
    run_migrations()
