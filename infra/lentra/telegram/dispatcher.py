import os
import time
import json
import requests
from lentra.telegram.db import get_conn

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def insert_task(conn, task_type, payload):
    try:
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO processing_queue (
                task_type,
                payload,
                status
            )
            VALUES (
                %s,
                %s,
                'pending'
            )
        """, (task_type, json.dumps(payload)))

        conn.commit()
        cur.close()

    except Exception as e:
        print("[DISPATCHER INSERT ERROR]", repr(e))


def get_updates(offset):
    url = f"{BASE_URL}/getUpdates"

    try:
        r = requests.get(
            url,
            params={"offset": offset, "timeout": 25},
            timeout=30
        )

        # 🔥 CRITICAL DEBUG (убирает слепые 404)
        print("[HTTP STATUS]", r.status_code)
        print("[RAW RESPONSE]", r.text[:300])

        return r.json()

    except Exception as e:
        print("[TG REQUEST ERROR]", repr(e))
        return {"ok": False, "result": []}


def main():
    print("[DISPATCHER SINGLE DB LAYER] STARTED")
    print("[BOT TOKEN]", BOT_TOKEN[:10], "...")

    if not BOT_TOKEN:
        print("[FATAL] BOT_TOKEN is empty")
        return

    conn = get_conn()
    offset = 0

    while True:
        data = get_updates(offset)

        if not isinstance(data, dict) or not data.get("ok"):
            print("[TG ERROR]", data)
            time.sleep(2)
            continue

        for u in data.get("result", []):
            offset = u.get("update_id", offset) + 1

            msg = u.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")

            print("[IN]", chat_id, text)

            if not text:
                continue

            insert_task(
                conn,
                "telegram_message",
                {
                    "chat_id": chat_id,
                    "text": text
                }
            )

        time.sleep(1)


if __name__ == "__main__":
    main()
