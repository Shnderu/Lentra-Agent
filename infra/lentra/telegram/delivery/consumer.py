import time
import psycopg2
import requests

DB_CONFIG = {
    "dbname": "lentra",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": 5432
}

BOT_TOKEN = "8963242841:AAFHQn4thrOcHGGdggiWOeiYA5OSv9jWeQE"


def claim():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload
        FROM processing_queue
        WHERE status = 'new'
        LIMIT 50
        FOR UPDATE SKIP LOCKED
    """)

    rows = cur.fetchall()
    ids = [r[0] for r in rows]

    if ids:
        cur.execute("""
            UPDATE processing_queue
            SET status = 'processing'
            WHERE id = ANY(%s)
        """, (ids,))

    conn.commit()
    cur.close()
    conn.close()

    return rows


def send(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    return requests.post(url, json={
        "chat_id": chat_id,
        "text": text
    }).json()


def mark_done(task_id):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'delivered'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()
    conn.close()


def main():
    print("[CONSUMER INTENT ROUTER V1] STARTED")

    while True:
        tasks = claim()

        if not tasks:
            time.sleep(1)
            continue

        for task_id, payload in tasks:

            # payload compatibility
            if "data" in payload:
                payload = payload["data"]

            chat_id = payload.get("chat_id")
            event = payload

            # IMPORT ROUTER FROM WORKER
            from lentra.telegram.worker import route

            result = route(event)

            text = result.get("text")

            if not chat_id or not text:
                print(f"[DROP] id={task_id}")
                continue

            resp = send(chat_id, text)

            if not resp.get("ok"):
                print("[SEND FAIL]", resp)
                continue

            mark_done(task_id)
            print(f"[DELIVERED] id={task_id}")

        time.sleep(1)


if __name__ == "__main__":
    main()
