from lentra.storage.db import get_conn


def is_processed(key: str) -> bool:
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 1
        FROM tasks
        WHERE idempotency_key = %s
          AND status = 'done'
        LIMIT 1
    """, (key,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row is not None


def mark_seen(task_id: str, key: str):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE tasks
        SET idempotency_key = %s
        WHERE id = %s
    """, (key, task_id))

    conn.commit()
    cur.close()
    conn.close()
