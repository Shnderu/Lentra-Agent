from core.db.connection import get_conn


def claim_tasks(worker_id: str, limit: int = 5):
    conn = get_conn()
    conn.autocommit = False
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, type, payload
            FROM tasks
            WHERE status = 'new'
              AND (run_after IS NULL OR run_after <= NOW())
            ORDER BY priority DESC, id ASC
            LIMIT %s
            FOR UPDATE SKIP LOCKED
        """, (limit,))

        rows = cur.fetchall()
        task_ids = [r["id"] for r in rows] if rows else []

        if task_ids:
            cur.execute("""
                UPDATE tasks
                SET status = 'processing',
                    locked_by = %s,
                    locked_at = NOW()
                WHERE id = ANY(%s)
            """, (worker_id, task_ids))

        conn.commit()
        return rows

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


def mark_done(task_id: int):
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


def mark_failed(task_id: int, error: str):
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE tasks
            SET status = 'failed',
                last_error = %s
            WHERE id = %s
        """, (error, task_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()
