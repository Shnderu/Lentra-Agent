import time
import psycopg2
import requests
import json
import os
from lentra.telegram.db import get_conn
from lentra.telegram.intent.router import route

BOT_TOKEN = os.getenv("BOT_TOKEN")


def send(chat_id, response):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": response.get("text", "")
    }

    # 🔥 ВАЖНО: добавляем UI если есть
    if "reply_markup" in response:
        payload["reply_markup"] = response["reply_markup"]

    return requests.post(url, json=payload).json()


def claim(conn):
    cur = conn.cursor()

    cur.execute("""
        SELECT id, payload
        FROM processing_queue
        WHERE status = 'pending'
        ORDER BY id ASC
        LIMIT 10
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

    return rows


def mark_done(conn, task_id):
    cur = conn.cursor()

    cur.execute("""
        UPDATE processing_queue
        SET status = 'delivered'
        WHERE id = %s
    """, (task_id,))

    conn.commit()
    cur.close()


def main():
    print("[CONSUMER UI FIXED STARTED]")

    conn = get_conn()

    while True:
        tasks = claim(conn)

        if not tasks:
            time.sleep(1)
            continue

        for task_id, payload in tasks:

            if isinstance(payload, str):
                payload = json.loads(payload)

            chat_id = payload.get("chat_id")

            result = route(payload)

            if not chat_id:
                continue

            resp = send(chat_id, result)

            if resp.get("ok"):
                mark_done(conn, task_id)
                print("[DELIVERED]", task_id)
            else:
                print("[SEND FAIL]", resp)

        time.sleep(1)


if __name__ == "__main__":
    main()
