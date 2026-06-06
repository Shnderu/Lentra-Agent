import json
from datetime import datetime
from core.db.connection import get_conn


# ---------------------------
# CREATE TASK
# ---------------------------
def push_task(task_type: str, payload: dict, priority: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks (type, payload, status, priority, retries, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            task_type,
            json.dumps(payload),
            "new",
            priority,
            0,
            datetime.utcnow(),
        ),
    )

    task_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return task_id


# ---------------------------
# CLAIM TASKS (worker picks)
# ---------------------------
def claim_tasks(worker_id: str, limit: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, type, payload
        FROM tasks
        WHERE status = 'new'
        ORDER BY priority DESC, id ASC
        LIMIT %s
        FOR UPDATE SKIP LOCKED
        """,
        (limit,),
    )

    rows = cur.fetchall()
    task_ids = [r[0] for r in rows]

    if task_ids:
        cur.execute(
            """
            UPDATE tasks
            SET status = 'processing',
                locked_by = %s,
                locked_at = NOW()
            WHERE id = ANY(%s)
            """,
            (worker_id, task_ids),
        )

    conn.commit()
    cur.close()
    conn.close()

    return rows


# ---------------------------
# MARK DONE
# ---------------------------
def mark_done(task_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET status = 'done'
        WHERE id = %s
        """,
        (task_id,),
    )

    conn.commit()
    cur.close()
    conn.close()


# ---------------------------
# MARK FAILED
# ---------------------------
def mark_failed(task_id: int, error: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET status = 'failed',
            last_error = %s,
            retries = retries + 1
        WHERE id = %s
        """,
        (error, task_id,),
    )

    conn.commit()
    cur.close()
    conn.close()
