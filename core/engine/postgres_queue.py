import os
import psycopg2
import psycopg2.extras
from typing import List, Dict, Any


# ----------------------------
# CONNECTION LAYER (RESTORED COMPATIBILITY)
# ----------------------------
def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "db"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "readme_to_recover"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD", "postgres"),
    )


# ----------------------------
# QUEUE LAYER (LEGACY + COMPAT)
# ----------------------------
def claim_tasks(worker_id: str, limit: int = 5) -> List[Dict[str, Any]]:
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:

            cur.execute(
                """
                UPDATE tasks
                SET status = 'processing',
                    locked_at = NOW(),
                    attempts = attempts + 1
                WHERE id IN (
                    SELECT id
                    FROM tasks
                    WHERE status = 'pending'
                      AND attempts < max_attempts
                    ORDER BY priority DESC, id ASC
                    LIMIT %s
                )
                RETURNING *;
                """,
                (limit,)
            )

            tasks = cur.fetchall()
            conn.commit()
            return tasks

    except Exception as e:
        conn.rollback()
        print(f"[QUEUE ERROR] claim_tasks: {e}")
        return []

    finally:
        conn.close()


def mark_done(task_id: int):
    conn = get_conn()
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

    finally:
        conn.close()


def mark_failed(task_id: int):
    conn = get_conn()
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

    finally:
        conn.close()


def recover_stuck_tasks(timeout_seconds: int = 300):
    conn = get_conn()
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

    finally:
        conn.close()
