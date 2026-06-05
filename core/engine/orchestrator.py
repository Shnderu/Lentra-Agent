import json
from core.db.connection import get_conn


# -------------------------
# TASK CREATION
# -------------------------
def insert_task(task_type, payload, retries=3):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (task_type, payload, retries)
        VALUES (%s, %s::jsonb, %s)
        RETURNING id
    """, (task_type, json.dumps(payload), retries))

    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return task_id


# -------------------------
# CLAIM TASK (CRITICAL PART)
# -------------------------
def claim_task(limit=1):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload, retries
        FROM tasks
        WHERE status = 'pending'
        ORDER BY id ASC
        FOR UPDATE SKIP LOCKED
        LIMIT %s
    """, (limit,))

    tasks = cur.fetchall()

    if tasks:
        ids = [t[0] for t in tasks]

        cur.execute("""
            UPDATE tasks
            SET status = 'processing', locked_at = NOW()
            WHERE id = ANY(%s)
        """, (ids,))

    conn.commit()
    cur.close()
    conn.close()

    return tasks


# -------------------------
# STATUS UPDATES
# -------------------------
def mark_done(task_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("UPDATE tasks SET status='done' WHERE id=%s", (task_id,))

    conn.commit()
    cur.close()
    conn.close()


def mark_failed(task_id, retries_left):
    conn = get_conn()
    cur = conn.cursor()

    if retries_left <= 0:
        cur.execute("UPDATE tasks SET status='dlq' WHERE id=%s", (task_id,))
    else:
        cur.execute("""
            UPDATE tasks
            SET status='pending', retries=%s
            WHERE id=%s
        """, (retries_left, task_id))

    conn.commit()
    cur.close()
    conn.close()
