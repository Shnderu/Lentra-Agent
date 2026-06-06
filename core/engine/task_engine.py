import json
from core.db.connection import get_conn


def normalize_payload(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True)


def safe_push_task(task_type: str, payload: dict, priority: int = 5):
    conn = get_conn()
    cur = conn.cursor()

    payload_str = normalize_payload(payload)

    # проверка дубля
    cur.execute(
        """
        SELECT id
        FROM tasks
        WHERE type = %s
          AND payload::text = %s
          AND status IN ('new','processing')
        LIMIT 1
        """,
        (task_type, payload_str),
    )

    exists = cur.fetchone()

    if exists:
        task_id = exists["id"] if isinstance(exists, dict) else exists[0]
        cur.close()
        conn.close()
        return task_id

    # создание задачи
    cur.execute(
        """
        INSERT INTO tasks (type, payload, status, priority, retries, created_at)
        VALUES (%s, %s, 'new', %s, 0, NOW())
        RETURNING id
        """,
        (task_type, payload_str, priority),
    )

    row = cur.fetchone()

    task_id = row["id"] if isinstance(row, dict) else row[0]

    conn.commit()
    cur.close()
    conn.close()

    return task_id
