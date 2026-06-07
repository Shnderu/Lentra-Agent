from core.db.connection import get_conn
import json


def safe_push_task(task_type: str, payload: dict, priority: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO tasks (type, payload, priority, status)
            VALUES (%s, %s::jsonb, %s, 'new')
            RETURNING id
            """,
            (
                task_type,
                json.dumps(payload),   # FIX: dict → json string
                priority
            )
        )

        task_id = cur.fetchone()[0]
        conn.commit()
        return task_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()


# совместимость (чтобы старые импорты не падали)
push_task = safe_push_task
