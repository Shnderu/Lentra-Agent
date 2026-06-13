import time
import json
import traceback
from lentra.storage.db import get_conn
from lentra.domain.property.search import search_properties
from lentra.ux.composer.engine import compose_properties
from lentra.telegram.ui.renderer import render_message


def fetch_task(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status = 'processing'
        ORDER BY id
        LIMIT 1
    """)

    row = cur.fetchone()
    cur.close()
    return row


def save_result(conn, task_id, result):
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'done',
            result = %s,
            processed_at = NOW()
        WHERE id = %s
    """, (json.dumps(result), task_id))

    conn.commit()
    cur.close()


def execute(task_type, payload):
    if task_type == "parse_property":
        props = search_properties(payload)
        ux = compose_properties(props)
        return {
            "ux": ux,
            "telegram_text": render_message(ux)
        }

    return {"telegram_text": "unsupported task"}


def main():
    print("[WORKER TELEGRAM UX] STARTED")

    while True:
        conn = get_conn()

        task = fetch_task(conn)

        if not task:
            time.sleep(0.5)
            continue

        task_id, task_type, payload = task

        try:
            print(f"[WORKER] EXEC task={task_id}")

            result = execute(task_type, payload)

            save_result(conn, task_id, result)

            print(f"[WORKER] DONE task={task_id}")

        except Exception as e:
            traceback.print_exc()

        finally:
            conn.close()
            time.sleep(0.1)


if __name__ == "__main__":
    main()
