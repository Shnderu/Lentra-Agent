import os
import psycopg2
from datetime import datetime, timedelta

DATABASE_URL = os.getenv("DATABASE_URL")

VISIBILITY_TIMEOUT_SEC = 60
MAX_ATTEMPTS = 5


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def claim_tasks(limit: int = 10):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        WITH cte AS (
            SELECT id
            FROM tasks
            WHERE
                (
                    status = 'done'
                    OR (
                        status = 'locked'
                        AND locked_at < NOW() - INTERVAL '60 seconds'
                    )
                )
                AND attempts < %s
            ORDER BY id
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        )
        UPDATE tasks t
        SET status = 'locked',
            locked_at = NOW()
        FROM cte
        WHERE t.id = cte.id
        RETURNING t.id, t.payload, t.result, t.attempts;
    """, (MAX_ATTEMPTS, limit))

    rows = cur.fetchall()
    conn.commit()
    conn.close()

    return rows


def mark_success(task_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'sent',
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    conn.close()


def mark_failure(task_id: int, error: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET attempts = attempts + 1,
            last_error = %s,
            status = CASE
                WHEN attempts + 1 >= %s THEN 'dead'
                ELSE 'done'
            END,
            updated_at = NOW()
        WHERE id = %s
    """, (error, MAX_ATTEMPTS, task_id))

    conn.commit()
    conn.close()
