# ============================================================
# LENTRA CONSUMER V2.1 (STABLE PIPELINE)
# ============================================================

import time
import json
import requests
import os
import hashlib

from lentra.telegram.db import get_conn
from lentra.telegram.intent.router import route
from lentra.observability.service import ObservabilityService
from lentra.telegram.delivery.queue_guard import release_stuck_tasks

BOT_TOKEN = os.getenv("BOT_TOKEN")

obs = ObservabilityService()

_last_render_hash = {}
_last_screen = {}


def send(chat_id, response):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": response.get("text", "")
    }

    if "reply_markup" in response:
        payload["reply_markup"] = response["reply_markup"]

    return requests.post(url, json=payload, timeout=10).json()


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
    print("[CONSUMER V2.1 STABLE STARTED]")

    conn = get_conn()

    while True:

        # 🔵 GUARD: release stuck tasks
        try:
            release_stuck_tasks(conn)
        except Exception as e:
            print("[QUEUE GUARD ERROR]", e)

        tasks = claim(conn)

        if not tasks:
            time.sleep(1)
            continue

        for task_id, payload in tasks:

            if isinstance(payload, str):
                payload = json.loads(payload)

            chat_id = payload.get("chat_id")
            trace_id = payload.get("trace_id") or str(task_id)

            trace = obs.start_trace(trace_id)
            obs.log_stage(trace, "CONSUMER_START", {"task_id": task_id})

            state = route(payload)
            obs.log_stage(trace, "ROUTER_DONE", state)

            screen = state.get("screen", "main")

            ui_payload = {
                "screen": screen,
                "state": state.get("state", {})
            }

            ui_hash = hashlib.md5(json.dumps(ui_payload, sort_keys=True).encode()).hexdigest()

            if _last_screen.get(chat_id) == screen:
                obs.log_stage(trace, "UI_SKIP_SAME_SCREEN")
                mark_done(conn, task_id)
                continue

            if _last_render_hash.get(chat_id) == ui_hash:
                obs.log_stage(trace, "UI_SKIP_DUPLICATE")
                mark_done(conn, task_id)
                continue

            result = render_response(screen)

            try:
                send_result = send(chat_id, result)
            except Exception as e:
                obs.log_stage(trace, "TELEGRAM_EXCEPTION", {"error": str(e)})
                continue

            obs.log_stage(trace, "TELEGRAM_SENT", send_result)

            if send_result.get("ok"):
                mark_done(conn, task_id)
                obs.log_stage(trace, "CONSUMER_DONE")

                _last_screen[chat_id] = screen
                _last_render_hash[chat_id] = ui_hash
            else:
                obs.log_stage(trace, "TELEGRAM_FAILED", send_result)

        time.sleep(1)


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
        return {"text": "🏠 Раздел аренды"}

    if screen == "search":
        return {"text": "🔎 Поиск жилья"}

    if screen == "profile":
        return {"text": "👤 Профиль"}

    return {"text": "🏠 Главное меню"}


if __name__ == "__main__":
    main()
