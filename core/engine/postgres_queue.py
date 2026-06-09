import psycopg2
import os
from datetime import datetime, timedelta

DB = {
    "host": os.getenv("DB_HOST", "db"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
}


def conn():
    c = psycopg2.connect(**DB)
    c.autocommit = True
    return c


def claim_tasks(worker_id, limit=5):
    c = conn()
    cur = c.cursor()

    cur.execute("SELECT pg_advisory_lock(123456)")

    cur.execute("""
        WITH picked AS (
            SELECT id
            FROM tasks
            WHERE status = 'pending'
              AND (next_retry_at IS NULL OR next_retry_at <= NOW())
            ORDER BY priority DESC, id
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        )
        UPDATE tasks t
        SET status='processing',
            worker_id=%s,
            started_at = COALESCE(started_at, NOW()),
            lease_until = NOW() + INTERVAL '2 minutes'
        FROM picked
        WHERE t.id = picked.id
        RETURNING t.id, t.task_type, t.payload, t.attempts, t.max_retries;
    """, (limit, worker_id))

    rows = cur.fetchall()

    cur.execute("SELECT pg_advisory_unlock(123456)")
    c.close()

    return rows


def mark_done(task_id):
    c = conn()
    cur = c.cursor()

    cur.execute("""
        UPDATE tasks
        SET status='done',
            finished_at=NOW()
        WHERE id=%s
    """, (task_id,))

    c.close()


def mark_failed(task_id, task_type, payload, error, attempts, max_retries):
    c = conn()
    cur = c.cursor()

    new_attempts = attempts + 1

    if new_attempts >= max_retries:
        # MOVE TO DLQ
        cur.execute("""
            INSERT INTO tasks_dlq(original_task_id, task_type, payload, error)
            VALUES (%s, %s, %s, %s)
        """, (task_id, task_type, payload, error))

        cur.execute("""
            UPDATE tasks
            SET status='dead',
                last_error=%s,
                attempts=%s,
                finished_at=NOW()
            WHERE id=%s
        """, (error, new_attempts, task_id))

    else:
        # RETRY WITH BACKOFF
        delay = min(60 * (2 ** new_attempts), 3600)

        cur.execute("""
            UPDATE tasks
            SET status='pending',
                last_error=%s,
                attempts=%s,
                next_retry_at = NOW() + (%s || ' seconds')::interval
            WHERE id=%s
        """, (error, new_attempts, delay, task_id))

    c.close()
