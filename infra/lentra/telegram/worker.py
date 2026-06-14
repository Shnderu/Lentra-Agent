import time
import json
import psycopg2

from lentra.domain.handlers.registry import HANDLERS

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[WORKER PROD] STARTED")


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
        SET
            result = %s::jsonb,
            status = 'done',
            processed_at = NOW()
        WHERE id = %s
    """, (
        json.dumps(result, ensure_ascii=False),
        task_id
    ))

    conn.commit()
    cur.close()


def save_error(task_id, err):
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET
            status = 'error',
            error_text = %s,
            processed_at = NOW()
        WHERE id = %s
    """, (
        str(err)[:5000],
        task_id
    ))

    conn.commit()
    cur.close()


def execute(task_type, payload):

    handler = HANDLERS.get(task_type)

    if not handler:
        return {
            "ux": {
                "screen": "error",
                "message": f"unknown task {task_type}"
            }
        }

    return handler(payload, {})


def main():

    while True:

        tasks = fetch_tasks()

        for task_id, task_type, payload in tasks:

            try:

                print(
                    f"[EXECUTE] "
                    f"id={task_id} "
                    f"type={task_type}"
                )

                result = execute(task_type, payload)

                if not isinstance(result, dict):
                    result = {
                        "ux": {
                            "screen": "error"
                        }
                    }

                save_result(task_id, result)

                print(f"[DONE] id={task_id}")

            except Exception as e:

                conn.rollback()

                save_error(task_id, e)

                print(
                    f"[ERROR] "
                    f"id={task_id} "
                    f"err={e}"
                )

        time.sleep(0.2)


if __name__ == "__main__":
    main()
