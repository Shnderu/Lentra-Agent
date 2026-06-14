import json
import requests
import psycopg2
import time
import uuid

BOT_TOKEN = "8963242841:AAFHQn4thrOcHGGdggiWOeiYA5OSv9jWeQE"

DB_CONFIG = {
    "dbname": "lentra",
    "user": "postgres",
    "password": "postgres",
    "host": "127.0.0.1",
    "port": 5432
}


def db_insert(event):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO processing_queue (task_type, payload, status)
        VALUES (%s, %s, %s)
    """, (
        "telegram_message",
        json.dumps(event),
        "new"
    ))

    conn.commit()
    cur.close()
    conn.close()


def fetch_updates(offset):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}"
    return requests.get(url).json()


def normalize(update):
    msg = update.get("message", {})

    trace_id = str(uuid.uuid4())

    return {
        "trace_id": trace_id,
        "chat_id": msg.get("chat", {}).get("id"),
        "text": msg.get("text"),
        "message_id": msg.get("message_id"),
        "raw": msg
    }


def main():
    print("[DISPATCHER OBSERVABILITY] STARTED")

    offset = 0

    while True:
        data = fetch_updates(offset)

        if not data.get("ok"):
            print("[TG ERROR]", data)
            time.sleep(2)
            continue

        for upd in data.get("result", []):
            offset = upd["update_id"] + 1

            event = normalize(upd)

            if event["chat_id"] and event["text"]:
                db_insert(event)
                print(f"[INGEST] trace={event['trace_id']} chat={event['chat_id']}")

        time.sleep(1)


if __name__ == "__main__":
    main()
