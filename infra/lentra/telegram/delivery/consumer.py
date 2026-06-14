import time
import json
import psycopg2

from lentra.telegram.delivery.sender import send_telegram
from lentra.telegram.ux.router import build_telegram_message

conn = psycopg2.connect(
    dbname="lentra",
    user="postgres",
    password="postgres",
    host="127.0.0.1",
    port=5432
)

print("[DELIVERY BOOLEAN FIX] STARTED")


def fetch():
    cur = conn.cursor()

    cur.execute("""
        SELECT id, result
        FROM processing_queue
        WHERE status='done'
          AND delivered = FALSE
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

        if rows:
            print(f"[CONSUMER] fetched={len(rows)}")

        for task_id, result in rows:

            try:

                if not result:
                    mark(task_id)
                    continue

                if isinstance(result, str):
                    result = json.loads(result)

                if not isinstance(result, dict):
                    mark(task_id)
                    continue

                ux = build_telegram_message(result)

                send_telegram(
                    chat_id=928857415,
                    text=ux.get("text", ""),
                    keyboard=ux.get("keyboard", [])
                )

                mark(task_id)

                print(f"[DELIVERED] id={task_id}")

            except Exception as e:

                conn.rollback()

                print(
                    f"[DELIVERY ERROR] "
                    f"id={task_id} "
                    f"err={e}"
                )

        time.sleep(0.5)


if __name__ == "__main__":
    main()
