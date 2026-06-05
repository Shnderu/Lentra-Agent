import os
import json
import psycopg2
from datetime import datetime, timedelta

DB = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DB)


# =========================
# ADD TASK
# =========================
def add_task(task_type: str, payload: dict, priority: int = 0):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (task_type, payload, priority)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (task_type, json.dumps(payload), priority))

    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return task_id


# =========================
# FETCH WITH LOCK (CRITICAL)
# =========================
def fetch_task():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload, retries, max_retries
        FROM tasks
        WHERE status = 'pending'
          AND run_after <= NOW()
        ORDER BY priority DESC, created_at ASC
        FOR UPDATE SKIP LOCKED
        LIMIT 1
    """)

    row = cur.fetchone()

    if not row:
        conn.close()
        return None

    task_id, task_type, payload, retries, max_retries = row

    cur.execute("""
        UPDATE tasks
        SET status = 'processing',
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": task_id,
        "type": task_type,
        "payload": payload,
        "retries": retries,
        "max_retries": max_retries
    }


# =========================
# MARK DONE
# =========================
def mark_done(task_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'done',
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()


# =========================
# MARK FAILED + RETRY
# =========================
def mark_failed(task):
    conn = get_conn()
    cur = conn.cursor()

    retries = task["retries"] + 1

    if retries >= task["max_retries"]:
        status = "failed"
        run_after = None
    else:
        status = "pending"
        run_after = datetime.utcnow() + timedelta(seconds=2 ** retries)

    cur.execute("""
        UPDATE tasks
        SET status = %s,
            retries = %s,
            run_after = %s,
            updated_at = NOW()
        WHERE id = %s
    """, (status, retries, run_after, task["id"]))

    conn.commit()
    cur.close()
    conn.close()
