import psycopg2
from psycopg2.extras import RealDictCursor
import time

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
                UPDATE tasks
                SET status = 'processing',
                    worker_id = %s,
                    locked_at = NOW(),
                    attempts = attempts + 1
                WHERE id IN (
                    SELECT id
                    FROM tasks
                    WHERE status = 'pending'
                    ORDER BY priority DESC, id ASC
                    LIMIT %s
                    FOR UPDATE SKIP LOCKED
                )
                RETURNING *;
            """, (worker_id, limit))

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
            SET status='done',
                worker_id=%s,
                updated_at=NOW()
            WHERE id=%s
        """, (worker_id, task_id))

    conn.close()


def mark_failed(task_id: int, worker_id: str, error: str):
    conn = get_connection()
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("""
            UPDATE tasks
            SET status='failed',
                worker_id=%s,
                updated_at=NOW()
            WHERE id=%s
        """, (worker_id, task_id))

    conn.close()
