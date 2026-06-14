import time
import psycopg2
import json

from lentra.domain.handlers.registry import HANDLERS
from lentra.domain.agent.brain import detect_intent, build_context

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[WORKER AGENT BRAIN V1] STARTED")


def fetch_tasks():
    cur = conn.cursor()

    cur.execute("""
        SELECT id, task_type, payload
        FROM processing_queue
        WHERE status='processing'
        ORDER BY id
        LIMIT 20
    """)

    rows = cur.fetchall()
    cur.close()

    return rows


def save_result(task_id, result):

    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET result = %s::jsonb,
            status = 'done',
            processed_at = NOW()
        WHERE id = %s
    """, (json.dumps(result, ensure_ascii=False), task_id))

    conn.commit()
    cur.close()


def execute(task_type, payload):

    handler = HANDLERS.get(task_type)

    if not handler:
        return {"ux": {"screen": "error"}}

    state = build_context(payload)

    return handler(payload, state)


def main():

    while True:

        tasks = fetch_tasks()

        for task_id, task_type, payload in tasks:

            print(f"[EXECUTE] {task_type} id={task_id}")

            result = execute(task_type, payload)

            if not isinstance(result, dict):
                result = {"ux": {"screen": "error"}}

            save_result(task_id, result)

            print(f"[DONE] id={task_id}")

        time.sleep(0.2)


if __name__ == "__main__":
    main()
