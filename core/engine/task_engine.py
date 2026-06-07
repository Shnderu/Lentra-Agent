from core.db.connection import get_conn
import json


def safe_push_task(task_type: str, payload: dict, priority: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO tasks (type, payload, priority)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (task_type, json.dumps(payload), priority))

        row = cur.fetchone()

        # 🔥 FIX: поддержка dict и tuple
        if isinstance(row, dict):
            task_id = row["id"]
        else:
            task_id = row[0]

        conn.commit()
        return task_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()
