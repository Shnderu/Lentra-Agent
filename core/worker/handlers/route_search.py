import asyncio
from core.bot.client import send_message
from core.queue.queue import ack, fail


async def handle(task):
    task_id = task["id"]
    payload = task["payload"]

    user_id = payload["user_id"]
    origin = payload.get("origin")
    destination = payload.get("destination")
    date = payload.get("date")

    try:
        print("[WORKER] route_search:", payload)

        # -------------------------
        # MOCK SEARCH (пока без API)
        # -------------------------
        result = (
            f"✈️ Результаты поиска\n\n"
            f"{origin} → {destination}\n"
            f"Дата: {date}\n\n"
            f"💺 Найдено 3 варианта (demo)"
        )

        await send_message(user_id, result)

        ack(task_id)

    except Exception as e:
        print("[WORKER ERROR]", e)
        fail(task_id)
