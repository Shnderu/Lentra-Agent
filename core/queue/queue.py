import os
import json
import uuid
import psycopg2
from datetime import datetime


def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))


# -------------------------
# ENQUEUE
# -------------------------
def enqueue(task_type: str, payload: dict):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks(type, payload)
        VALUES (%s, %s)
        RETURNING id
    """, (task_type, json.dumps(payload)))

    task_id = cur.fetchone()[0]

    conn.commit()
    conn.close()

    return task_id


# -------------------------
# CLAIM TASK (LOCK SAFE)
# -------------------------
def claim(worker_id: str, limit: int = 1):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, type, payload
        FROM tasks
        WHERE status = 'queued'
          AND run_after <= NOW()
        ORDER BY id
        FOR UPDATE SKIP LOCKED
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    tasks = []

    for r in rows:
        task_id = r[0]

        cur.execute("""
            UPDATE tasks
            SET status = 'processing',
                locked_at = NOW(),
                locked_by = %s,
                updated_at = NOW()
            WHERE id = %s
        """, (worker_id, task_id))

        tasks.append({
            "id": task_id,
            "type": r[1],
            "payload": r[2]
        })

    conn.commit()
    conn.close()

    return tasks


# -------------------------
# ACK SUCCESS
# -------------------------
def ack(task_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'done',
            updated_at = NOW()
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    conn.close()


# -------------------------
# FAIL + RETRY
# -------------------------
def fail(task_id: int, retry_delay_sec: int = 30):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = CASE
            WHEN attempts >= 3 THEN 'dead'
            ELSE 'queued'
        END,
        attempts = attempts + 1,
        run_after = NOW() + (%s || ' seconds')::interval,
        updated_at = NOW()
        WHERE id = %s
    """, (retry_delay_sec, task_id))

    conn.commit()
    conn.close()
