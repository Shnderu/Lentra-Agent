import time
import json
import psycopg2

from lentra.domain.handlers.registry import HANDLERS
from lentra.domain.handlers.fallback import handle_unknown


conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[WORKER PRODUCT LAYER FIXED JSON] STARTED")


def fetch_tasks():
    cur = conn.cursor()
    cur.execute("""
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status='processing'
        ORDER BY id
        LIMIT 10
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def save_result(task_id, result):
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET result = %s,
            status = 'done'
        WHERE id = %s
    """, (json.dumps(result), task_id))

    conn.commit()
    cur.close()


def execute_task(task_type, payload):
    handler = HANDLERS.get(task_type)

    if not handler:
        return handle_unknown(task_type, payload)

    return handler(payload)


def main():
    while True:
        tasks = fetch_tasks()

        for task_id, task_type, payload in tasks:

            print(f"[EXECUTE] type={task_type} id={task_id}")

            result = execute_task(task_type, payload)

            print(f"[EXECUTE RESULT]={result}")

            save_result(task_id, result)

            print(f"[DONE] task={task_id}")

        time.sleep(0.2)


if __name__ == "__main__":
    main()
