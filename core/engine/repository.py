import json
import psycopg2
from core.db.connection import get_conn


def fetch_tasks(worker_id, limit=10):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload
        FROM tasks
        WHERE status = 'pending'
        ORDER BY priority DESC, created_at ASC
        LIMIT %s
    """, (limit,))

    rows = cur.fetchall()

    tasks = []
    for r in rows:
        tasks.append({
            "id": r[0],
            "payload": r[1]
        })

    cur.close()
    conn.close()
    return tasks


def mark_done(task_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'done'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()


def mark_failed(task_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'failed'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()
