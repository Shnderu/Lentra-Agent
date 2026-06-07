import psycopg2
from contextlib import contextmanager
from core.db.connection import get_conn


@contextmanager
def conn():
    c = get_conn()
    try:
        c.autocommit = True
        yield c
    finally:
        c.close()


def claim_tasks(worker_id: str, limit: int = 5):
    """
    Atomic + safe claim (NO race conditions)
    """

    with conn() as c:
        cur = c.cursor()

        cur.execute(
            """
            WITH cte AS (
                SELECT id
                FROM tasks
                WHERE status = 'pending'
                  AND attempts < max_attempts
                ORDER BY priority DESC, created_at ASC
                FOR UPDATE SKIP LOCKED
                LIMIT %s
            )
            UPDATE tasks t
            SET status = 'processing',
                worker_id = %s,
                locked_at = NOW(),
                updated_at = NOW(),
                attempts = attempts + 1
            FROM cte
            WHERE t.id = cte.id
            RETURNING t.id, t.task_type, t.payload;
            """,
            (limit, worker_id)
        )

        return cur.fetchall()


def mark_done(task_id: int):
    with conn() as c:
        cur = c.cursor()
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
    with conn() as c:
        cur = c.cursor()
        cur.execute(
            """
            UPDATE tasks
            SET status = CASE
                WHEN attempts >= max_attempts THEN 'dead'
                ELSE 'pending'
            END,
            last_error = %s,
            updated_at = NOW()
            WHERE id = %s
            """,
            (error, task_id)
        )


def recover_stuck_tasks(timeout_seconds: int = 300):
    """
    Возвращает зависшие processing задачи обратно в очередь
    """
    with conn() as c:
        cur = c.cursor()

        cur.execute(
            """
            UPDATE tasks
            SET status = 'pending',
                worker_id = NULL,
                locked_at = NULL
            WHERE status = 'processing'
              AND locked_at < NOW() - INTERVAL '%s seconds'
            """,
            (timeout_seconds,)
        )
