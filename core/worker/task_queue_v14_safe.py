import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def claim_tasks(limit: int = 10):
    conn = None
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            WITH cte AS (
                SELECT id
                FROM tasks
                WHERE status = 'done'
                OR (
                    status = 'locked'
                    AND locked_at < NOW() - INTERVAL '60 seconds'
                )
                AND attempts < 5
                ORDER BY id
                LIMIT %s
                FOR UPDATE SKIP LOCKED
            )
            UPDATE tasks t
            SET status = 'locked',
                locked_at = NOW()
            FROM cte
            WHERE t.id = cte.id
            RETURNING t.id, t.payload, t.result, t.attempts;
        """, (limit,))

        rows = cur.fetchall()
        conn.commit()
        return rows

    except Exception as e:
        print("[CLAIM ERROR]", e)
        return []

    finally:
        try:
            if conn:
                conn.close()
        except:
            pass


def mark_success(task_id: int):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET status='sent',
                updated_at=NOW()
            WHERE id=%s
        """, (task_id,))

        conn.commit()
        conn.close()
    except Exception as e:
        print("[MARK SUCCESS ERROR]", e)


def mark_failure(task_id: int, error: str):
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET attempts = attempts + 1,
                last_error = %s,
                status = CASE
                    WHEN attempts + 1 >= 5 THEN 'dead'
                    ELSE 'done'
                END,
                updated_at = NOW()
            WHERE id = %s
        """, (error, task_id))

        conn.commit()
        conn.close()
    except Exception as e:
        print("[MARK FAIL ERROR]", e)
