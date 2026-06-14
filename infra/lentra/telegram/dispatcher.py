import os
import time
import json
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from lentra.telegram.db import get_conn

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# 🔥 STABLE SESSION (FIX HANGS)
session = requests.Session()

retry = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry, pool_connections=10, pool_maxsize=10)
session.mount("https://", adapter)


def verify():
    r = session.get(f"{BASE_URL}/getMe", timeout=(3, 10))
    print("[BOT CHECK]", r.json())


def insert_task(conn, task_type, payload):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO processing_queue (task_type, payload, status)
            VALUES (%s, %s, 'pending')
        """, (task_type, json.dumps(payload)))
    conn.commit()


def get_updates(offset):
    try:
        r = session.get(
            f"{BASE_URL}/getUpdates",
            params={"offset": offset, "timeout": 5},
            timeout=(3, 8)
        )
        print("[HTTP DONE]")
        print("[HTTP STATUS]", r.status_code)

        return r.json()

    except Exception as e:
        print("[HTTP ERROR]", repr(e))
        return {"ok": False, "result": []}


def main():
    print("[DISPATCHER STARTED]")
    verify()

    offset = 0

    while True:
        try:
            print("[LOOP TICK]")

            conn = get_conn()
            print("[DB OK]")

            data = get_updates(offset)

            if not data.get("ok"):
                print("[TG ERROR]", data)
                time.sleep(2)
                continue

            for u in data.get("result", []):
                offset = u["update_id"] + 1

                msg = u.get("message", {})
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "")

                print("[IN]", chat_id, text)

                insert_task(conn, "telegram_message", {
                    "chat_id": chat_id,
                    "text": text
                })

            conn.close()
            time.sleep(1)

        except Exception as e:
            print("[LOOP ERROR]", repr(e))
            time.sleep(2)


if __name__ == "__main__":
    main()
