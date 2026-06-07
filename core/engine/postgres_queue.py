import os
import psycopg2
import psycopg2.extras
from typing import List, Dict, Any


# =========================================================
# CONNECTION LAYER (SINGLE SOURCE OF TRUTH)
# =========================================================

def get_conn():
    """
    Production-safe DB connection factory.
    Используется worker / router / handlers.
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "readme_to_recover"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


# =========================================================
# TASK CLAIMING (ATOMIC QUEUE LOCK)
# =========================================================

def claim_tasks(conn, worker_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    """
    Атомарно забирает задачи в работу.
    Исключает гонки через SKIP LOCKED.
    """

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

            cur.execute(
                """
                WITH picked AS (
                    SELECT id
                    FROM tasks
                    WHERE status = 'pending'
                      AND attempts < max_attempts
                    ORDER BY priority DESC, id ASC
                    FOR UPDATE SKIP LOCKED
                    LIMIT %s
                )
                UPDATE tasks t
                SET status = 'processing',
                    locked_at = NOW(),
                    attempts = attempts + 1
                FROM picked
                WHERE t.id = picked.id
                RETURNING t.*;
                """,
                (limit,)
            )

            rows = cur.fetchall()
            conn.commit()
            return rows

    except Exception as e:
        conn.rollback()
        print(f"[QUEUE ERROR] claim_tasks: {e}")
        return []


# =========================================================
# TASK FINALIZATION
# =========================================================

def mark_done(conn, task_id: int):
    """
    Завершение задачи.
    """

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'done',
                    updated_at = NOW()
                WHERE id = %s
                """,
                (task_id,)
            )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"[QUEUE ERROR] mark_done: {e}")


def mark_failed(conn, task_id: int):
    """
    Фиксация падения задачи.
    """

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'failed',
                    updated_at = NOW()
                WHERE id = %s
                """,
                (task_id,)
            )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"[QUEUE ERROR] mark_failed: {e}")


# =========================================================
# RECOVERY MECHANISM
# =========================================================

def recover_stuck_tasks(conn, timeout_seconds: int = 300):
    """
    Возвращает зависшие processing-задачи обратно в pending.
    """

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE tasks
                SET status = 'pending',
                    locked_at = NULL
                WHERE status = 'processing'
                  AND locked_at < NOW() - INTERVAL '%s seconds'
                """,
                (timeout_seconds,)
            )
        conn.commit()

    except Exception as e:
        conn.rollback()
        print(f"[QUEUE ERROR] recover_stuck_tasks: {e}")
