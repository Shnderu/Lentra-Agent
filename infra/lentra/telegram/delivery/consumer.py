import time
import psycopg2
import requests
import json
import os
import hashlib

from lentra.telegram.db import get_conn
from lentra.telegram.intent.router import route

BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔵 UI CACHE (in-memory)
_last_render_hash = {}
_last_screen = {}


def _hash_ui(payload: dict) -> str:
    raw = json.dumps(payload, sort_keys=True)
    return hashlib.md5(raw.encode()).hexdigest()


def send(chat_id, response):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": response.get("text", "")
    }

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

            if not chat_id:
                continue

            # 🔵 ROUTER → STATE → UI
            state = route(payload)

            screen = state.get("screen", "main")

            # 🔥 UI CACHE KEY
            ui_payload = {
                "screen": screen,
                "state": state.get("state", {})
            }

            ui_hash = _hash_ui(ui_payload)

            # 🔥 1. SCREEN GUARD (no repeat render)
            if _last_screen.get(chat_id) == screen:
                print("[UI SKIP] same screen:", screen)
                mark_done(conn, task_id)
                continue

            # 🔥 2. RENDER GUARD (no duplicate UI)
            if _last_render_hash.get(chat_id) == ui_hash:
                print("[UI SKIP] duplicate render hash")
                mark_done(conn, task_id)
                continue

            # 🔵 BUILD RESPONSE
            result = render_response(screen=screen)

            resp = send(chat_id, result)

            if resp.get("ok"):
                mark_done(conn, task_id)

                _last_screen[chat_id] = screen
                _last_render_hash[chat_id] = ui_hash

                print("[DELIVERED]", task_id)
            else:
                print("[SEND FAIL]", resp)

        time.sleep(1)


# 🔵 SIMPLE UI RENDER (TEMP CONTRACT)
def render_response(screen: str) -> dict:
    if screen == "main":
        return {
            "text": "🏠 Главное меню",
            "reply_markup": {
                "keyboard": [
                    ["🏠 Аренда", "🔎 Поиск"],
                    ["📊 Уведомления", "👤 Профиль"]
                ],
                "resize_keyboard": True
            }
        }

    if screen == "rent":
        return {
            "text": "🏠 Раздел аренды",
            "reply_markup": {
                "keyboard": [
                    ["🔎 Поиск", "⬅️ Назад"]
                ],
                "resize_keyboard": True
            }
        }

    if screen == "search":
        return {
            "text": "🔎 Поиск жилья",
            "reply_markup": {
                "keyboard": [
                    ["🏠 Аренда", "⬅️ Назад"]
                ],
                "resize_keyboard": True
            }
        }

    if screen == "profile":
        return {
            "text": "👤 Профиль пользователя",
            "reply_markup": {
                "keyboard": [
                    ["🏠 Главное меню"]
                ],
                "resize_keyboard": True
            }
        }

    return {
        "text": "🏠 Главное меню",
        "reply_markup": {
            "keyboard": [
                ["🏠 Аренда", "🔎 Поиск"],
                ["📊 Уведомления", "👤 Профиль"]
            ],
            "resize_keyboard": True
        }
    }


if __name__ == "__main__":
    main()
