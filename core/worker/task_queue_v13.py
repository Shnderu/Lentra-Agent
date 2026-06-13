import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def claim_tasks(limit: int = 10):
    """
    Атомарно забирает задачи в статусе done → locked
    Гарантия: один воркер = одна задача
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        WITH cte AS (
            SELECT id
            FROM tasks
            WHERE status = 'done'
            ORDER BY id
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        )
        UPDATE tasks t
        SET status = 'locked',
            locked_at = NOW()
        FROM cte
        WHERE t.id = cte.id
        RETURNING t.id, t.payload, t.result;
    """, (limit,))

    rows = cur.fetchall()
    conn.commit()
    conn.close()

    return rows


def mark_done(task_id: int):
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


def mark_failed(task_id: int, error: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET status = 'failed',
            result = %s,
            updated_at = NOW()
        WHERE id = %s
    """, (error, task_id))

    conn.commit()
    conn.close()
