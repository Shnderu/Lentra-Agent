import json
import socket
from datetime import datetime, timedelta

from core.db.connection import get_conn


WORKER_ID = socket.gethostname()


# -------------------------
# INSERT TASK
# -------------------------
def insert_task(task_type, payload, priority=5, retries=3):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (task_type, payload, priority, retries)
        VALUES (%s, %s::jsonb, %s, %s)
        RETURNING id
    """, (task_type, json.dumps(payload), priority, retries))

    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return task_id


# -------------------------
# CLAIM DISTRIBUTED TASKS
# -------------------------
def claim_tasks(limit=5):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload, retries
        FROM tasks
        WHERE status = 'pending'
          AND run_after <= NOW()
        ORDER BY priority ASC, id ASC
        FOR UPDATE SKIP LOCKED
        LIMIT %s
    """, (limit,))

    tasks = cur.fetchall()

    if tasks:
        ids = [t[0] for t in tasks]

        cur.execute("""
            UPDATE tasks
            SET status = 'processing',
                locked_at = NOW(),
                locked_by = %s
            WHERE id = ANY(%s)
        """, (WORKER_ID, ids))

    conn.commit()
    cur.close()
    conn.close()

    return tasks


# -------------------------
# COMPLETE TASK
# -------------------------
def mark_done(task_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status='done'
        WHERE id=%s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()


# -------------------------
# FAIL + RETRY BACKOFF
# -------------------------
def mark_failed(task_id, retries_left):
    conn = get_conn()
    cur = conn.cursor()

    if retries_left <= 0:
        cur.execute("""
            UPDATE tasks
            SET status='dlq'
            WHERE id=%s
        """, (task_id,))
    else:
        backoff = datetime.utcnow() + timedelta(seconds=2 ** (3 - retries_left))

        cur.execute("""
            UPDATE tasks
            SET status='pending',
                retries=%s,
                run_after=%s
            WHERE id=%s
        """, (retries_left, backoff, task_id))

    conn.commit()
    cur.close()
    conn.close()


# -------------------------
# REAPER (cleanup stuck tasks)
# -------------------------
def requeue_stuck(seconds=60):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status='pending',
            locked_at=NULL,
            locked_by=NULL
        WHERE status='processing'
          AND locked_at < NOW() - INTERVAL '%s seconds'
    """, (seconds,))

    conn.commit()
    cur.close()
    conn.close()
