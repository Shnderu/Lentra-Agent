import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta

DB_CONFIG = {
    "host": "db",
    "dbname": "readme_to_recover",
    "user": "postgres",
    "password": "postgres",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def claim_tasks(worker_id: str, limit: int = 5):
    conn = None
    try:
        conn = get_connection()
        conn.autocommit = True

        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                WITH cte AS (
                    SELECT id
                    FROM tasks
                    WHERE status = 'pending'
                      AND (retry_at IS NULL OR retry_at <= NOW())
                    ORDER BY priority DESC, id ASC
                    LIMIT %s
                    FOR UPDATE SKIP LOCKED
                )
                UPDATE tasks t
                SET status = 'processing',
                    worker_id = %s,
                    locked_at = NOW(),
                    attempts = attempts + 1,
                    updated_at = NOW()
                FROM cte
                WHERE t.id = cte.id
                RETURNING t.*;
            """, (limit, worker_id))

            return cur.fetchall()

    except Exception as e:
        print(f"[QUEUE ERROR] {e}")
        return []

    finally:
        if conn:
            conn.close()


def mark_done(task_id: int, worker_id: str):
    conn = get_connection()
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE tasks
            SET status = 'done',
                worker_id = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (worker_id, task_id))

    conn.close()


def mark_failed(task_id: int, worker_id: str, error: str):
    conn = get_connection()
    conn.autocommit = True

    with conn.cursor(cursor_factory=RealDictCursor) as cur:

        # получаем текущие attempts
        cur.execute("""
            SELECT attempts, max_attempts
            FROM tasks
            WHERE id = %s
        """, (task_id,))

        row = cur.fetchone()

        if not row:
            return

        attempts = row["attempts"]
        max_attempts = row["max_attempts"]

        # если превышен лимит → dead
        if attempts >= max_attempts:
            cur.execute("""
                UPDATE tasks
                SET status = 'dead',
                    worker_id = %s,
                    updated_at = NOW()
                WHERE id = %s
            """, (worker_id, task_id))
            return

        # exponential backoff (30s, 2m, 10m, 30m...)
        delay = min(60 * (2 ** attempts), 1800)

        retry_at = datetime.utcnow() + timedelta(seconds=delay)

        cur.execute("""
            UPDATE tasks
            SET status = 'pending',
                worker_id = %s,
                retry_at = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (worker_id, retry_at, task_id))

    conn.close()
