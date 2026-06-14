import time
import psycopg2
import json

from lentra.telegram.ux.router.build_telegram_message import build_telegram_message
from lentra.telegram.ux.renderers.telegram_renderer import render_telegram_message
from lentra.telegram.delivery.sender import send_telegram
from lentra.telegram.ux.router.executor import execute_callback


conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[DELIVERY AGENT LOOP V1] STARTED")


def fetch():
    cur = conn.cursor()
    cur.execute("""
        SELECT id, result, chat_id
        FROM processing_queue
        WHERE status='done'
          AND delivered IS NULL
        ORDER BY id
        LIMIT 20
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def mark(task_id):
    cur = conn.cursor()
    cur.execute("""
        UPDATE processing_queue
        SET delivered = TRUE
        WHERE id = %s
    """, (task_id,))
    conn.commit()
    cur.close()


def main():

    while True:

        rows = fetch()

        for task_id, result, chat_id in rows:

            if not result:
                mark(task_id)
                continue

            if isinstance(result, str):
                try:
                    result = json.loads(result)
                except:
                    mark(task_id)
                    continue

            # STEP 6 — callback execution layer
            callback = result.get("ux", {}).get("callback_data")

            if callback:
                result = execute_callback(chat_id or 0, callback)

            ux = build_telegram_message(result)
            tg = render_telegram_message(ux)

            send_telegram(
                chat_id=chat_id or 928857415,
                text=tg["text"],
                keyboard=tg["keyboard"]
            )

            mark(task_id)

            print(f"[DELIVERED AGENT] id={task_id}")

        time.sleep(0.5)


if __name__ == "__main__":
    main()
