import requests
import time
import json
import os
from lentra.telegram.db import get_conn

BOT_TOKEN = os.getenv("BOT_TOKEN")

def insert_task(chat_id, event_type, payload):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO processing_queue (chat_id, event_type, payload, status)
        VALUES (%s, %s, %s, 'pending')
    """, (chat_id, event_type, json.dumps(payload)))

    conn.commit()
    cur.close()
    conn.close()

def main():
    offset = 0
    print("[DISPATCHER SINGLE DB LAYER] STARTED")

    while True:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?offset={offset}"
        r = requests.get(url).json()

        if r.get("ok"):
            for u in r["result"]:
                offset = u["update_id"] + 1

                msg = u.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")

                if chat_id:
                    insert_task(chat_id, text, {"text": text})

        time.sleep(1)

if __name__ == "__main__":
    main()
