import asyncio
import asyncpg
import os
import traceback
import json

from app.core.gateway.execution_entry_v1 import execute as gateway_execute
from lentra.db.queue import PostgresQueue
from lentra.services.telegram_notifier import TelegramNotifier

DB_DSN = os.getenv("DB_DSN")

# =========================
# DELIVERY LAYER (NEW)
# =========================
notifier = TelegramNotifier()
notifier.start()


def _extract_chat_id(task: dict):
    """
    Safe extraction from different payload formats
    """
    try:
        payload = task.get("payload", {})
        if isinstance(payload, str):
            payload = json.loads(payload)

        return payload.get("chat_id")
    except Exception:
        return None


def _render_result(result: dict) -> str:
    """
    Minimal renderer (can be replaced later with UX layer)
    """
    if not result:
        return "Пустой результат"

    if isinstance(result, dict):
        if result.get("type") == "rent_search":
            items = result.get("results", [])
            return "\n".join(
                f"🏠 {i.get('title', 'no-title')} | {i.get('price', '')}"
                for i in items[:5]
            )

        if result.get("type") == "fallback":
            return "⚠️ fallback сценарий"

    return str(result)


async def process_task(task):
    """
    All flows go through gateway + delivery
    """

    result = gateway_execute(task)

    print(f"[WORKER] {task['task_type']} -> {result.get('ok', True)}")
    print("[WORKER RESULT RAW]:", result)

    # =========================
    # TELEGRAM DELIVERY FIX
    # =========================
    chat_id = _extract_chat_id(task)

    if chat_id:
        try:
            text = _render_result(result)
            notifier.send(chat_id, text)
            print(f"[WORKER] TELEGRAM SENT -> chat_id={chat_id}")
        except Exception as e:
            print("[WORKER TELEGRAM ERROR]", str(e))
            traceback.print_exc()
    else:
        print("[WORKER] NO CHAT_ID FOUND - SKIP DELIVERY")


async def worker_loop():
    pool = await asyncpg.create_pool(dsn=DB_DSN, min_size=1, max_size=10)
    queue = PostgresQueue(pool)

    print("[WORKER] STARTED")

    while True:
        try:
            task = await queue.claim_task()

            if not task:
                await asyncio.sleep(1)
                continue

            try:
                await process_task(task)
                await queue.mark_done(task["id"])

            except Exception as e:
                print("[WORKER TASK ERROR]", str(e))
                traceback.print_exc()
                await queue.mark_failed(task["id"], str(e))

        except Exception as e:
            print("[WORKER LOOP ERROR]", str(e))
            traceback.print_exc()
            await asyncio.sleep(2)


async def main():
    while True:
        try:
            await worker_loop()
        except Exception as e:
            print("[WORKER FATAL RESTART]", str(e))
            traceback.print_exc()
            await asyncio.sleep(3)


if __name__ == "__main__":
    asyncio.run(main())
