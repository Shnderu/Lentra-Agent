import psycopg2
import json
import os

DB = os.getenv("DATABASE_URL")


def get_conn():
    if not DB:
        raise RuntimeError("DATABASE_URL is missing")

    return psycopg2.connect(DB)


def create_task(task_type, payload, priority=1):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (type, payload, priority)
        VALUES (%s, %s, %s)
    """, (task_type, json.dumps(payload), priority))

    conn.commit()
    cur.close()
    conn.close()


def fetch_task():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, type, payload, retries, max_retries
        FROM tasks
        WHERE status = 'pending'
        ORDER BY priority DESC, created_at ASC
        LIMIT 1
        FOR UPDATE SKIP LOCKED
    """)

    row = cur.fetchone()

    if not row:
        conn.commit()
        cur.close()
        conn.close()
        return None

    task_id, ttype, payload, retries, max_retries = row

    cur.execute("""
        UPDATE tasks SET status = 'processing'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()

    return {
        "id": task_id,
        "type": ttype,
        "payload": payload,
        "retries": retries,
        "max_retries": max_retries
    }


def complete_task(task_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks SET status = 'done'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()


def fail_task(task):
    conn = get_conn()
    cur = conn.cursor()

    new_retry = task["retries"] + 1

    status = "failed" if new_retry >= task["max_retries"] else "pending"

    cur.execute("""
        UPDATE tasks
        SET status = %s,
            retries = %s
        WHERE id = %s
    """, (status, new_retry, task["id"]))

    conn.commit()
    cur.close()
    conn.close()
