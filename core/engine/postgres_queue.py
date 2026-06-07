import time
import psycopg2
from contextlib import contextmanager
from core.db.connection import get_conn


@contextmanager
def _conn():
    conn = get_conn()
    try:
        conn.autocommit = True
        yield conn
    finally:
        conn.close()


def claim_tasks(worker_id: str, limit: int = 5):
    """
    SAFE CLAIM (без гонок)
    """
    with _conn() as conn:
        cur = conn.cursor()

        cur.execute(
            """
            WITH cte AS (
                SELECT id
                FROM tasks
                WHERE status = 'pending'
                ORDER BY priority DESC, id ASC
                FOR UPDATE SKIP LOCKED
                LIMIT %s
            )
            UPDATE tasks t
            SET status = 'processing',
                worker_id = %s,
                updated_at = NOW()
            FROM cte
            WHERE t.id = cte.id
            RETURNING t.*;
            """,
            (limit, worker_id)
        )

        return cur.fetchall()


def mark_done(task_id: int):
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE tasks
            SET status = 'done',
                updated_at = NOW()
            WHERE id = %s
            """,
            (task_id,)
        )


def mark_failed(task_id: int, error: str):
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE tasks
            SET status = 'failed',
                error = %s,
                updated_at = NOW()
            WHERE id = %s
            """,
            (error, task_id)
        )
