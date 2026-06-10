import psycopg2
import json
import os
import time


# -----------------------------
# CONNECTION RESET (CRITICAL)
# -----------------------------
def get_conn():
    """
    Production-safe connection with reset logic.
    Prevents stale connections in long-running worker.
    """
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    conn.autocommit = False
    return conn


def _reset_conn(conn):
    """
    Hard reset connection (required for long-running worker stability)
    """
    try:
        conn.rollback()
    except Exception:
        pass
    try:
        conn.close()
    except Exception:
        pass


# -----------------------------
# ENQUEUE
# -----------------------------
def enqueue(task_type: str, payload: dict):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO tasks (type, payload, status, run_after)
            VALUES (%s, %s, 'queued', NOW())
            RETURNING id
        """, (task_type, json.dumps(payload)))

        task_id = cur.fetchone()[0]
        conn.commit()
        return task_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        _reset_conn(conn)


# -----------------------------
# CLAIM (CRITICAL FIX)
# -----------------------------
def claim(worker_id: str = "worker"):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE tasks
            SET status = 'processing',
                locked_by = %s
            WHERE id = (
                SELECT id FROM tasks
                WHERE status = 'queued'
                AND run_after <= NOW()
                ORDER BY id ASC
                LIMIT 1
                FOR UPDATE SKIP LOCKED
            )
            RETURNING id, type, payload
        """, (worker_id,))

        row = cur.fetchone()

        conn.commit()

        if not row:
            return []

        payload = row[2]

        if isinstance(payload, str):
            payload = json.loads(payload)

        return [{
            "id": row[0],
            "type": row[1],
            "payload": payload
        }]

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        _reset_conn(conn)


# -----------------------------
# MARK DONE
# -----------------------------
def mark_done(task_id: int, result: str):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE tasks
            SET status = 'done',
                result = %s
            WHERE id = %s
        """, (result, task_id))

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        _reset_conn(conn)


# -----------------------------
# MARK FAILED
# -----------------------------
def mark_failed(task_id: int, error: str):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE tasks
            SET status = 'failed',
                error = %s
            WHERE id = %s
        """, (error, task_id))

        conn.commit()

    except Exception:
        conn.rollback()

    finally:
        _reset_conn(conn)


# -----------------------------
# MARK SENT (for bot notifications if needed)
# -----------------------------
def mark_sent(task_id: int):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            UPDATE tasks
            SET status = 'sent'
            WHERE id = %s
        """, (task_id,))

        conn.commit()

    except Exception:
        conn.rollback()

    finally:
        _reset_conn(conn)
