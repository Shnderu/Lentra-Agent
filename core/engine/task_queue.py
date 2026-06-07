from core.db.connection import get_conn
import json


def create_task(task_type, payload, priority=1):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO tasks (type, payload, priority, status)
            VALUES (%s, %s::jsonb, %s, 'new')
        """, (task_type, json.dumps(payload), priority))

        conn.commit()

    finally:
        cur.close()
        conn.close()


def fetch_task():
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, type, payload, retries, max_retries
            FROM tasks
            WHERE status = 'new'
            ORDER BY priority DESC, id ASC
            LIMIT 1
            FOR UPDATE SKIP LOCKED
        """)

        row = cur.fetchone()

        if not row:
            conn.commit()
            return None

        task_id, ttype, payload, retries, max_retries = row

        cur.execute("""
            UPDATE tasks
            SET status = 'processing'
            WHERE id = %s
        """, (task_id,))

        conn.commit()

        return {
            "id": task_id,
            "type": ttype,
            "payload": payload,
            "retries": retries,
            "max_retries": max_retries
        }

    finally:
        cur.close()
        conn.close()


def complete_task(task_id):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE tasks
            SET status = 'done'
            WHERE id = %s
        """, (task_id,))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def fail_task(task):
    conn = get_conn()
    cur = conn.cursor()

    try:
        new_retry = task["retries"] + 1
        status = "failed" if new_retry >= task["max_retries"] else "new"

        cur.execute("""
            UPDATE tasks
            SET status = %s,
                retries = %s
            WHERE id = %s
        """, (status, new_retry, task["id"]))

        conn.commit()

    finally:
        cur.close()
        conn.close()
