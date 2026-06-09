from core.queue.queue import ack, fail
from core.flight_engine.service import FlightSearchService
from core.bot.client import send_message

service = FlightSearchService()


async def handle(task: dict):

    task_id = task["id"]
    payload = task["payload"]

    user_id = payload["user_id"]

    try:
        results = await service.search(
            payload["origin"],
            payload["destination"],
            payload["date"]
        )

        text = "✈️ Лучшие варианты\n\n"

        if not results:
            text += "Рейсов не найдено"
        else:
            for r in results[:5]:
                text += (
                    f"{r['airline']} ({r['provider']})\n"
                    f"{r['from']} → {r['to']}\n"
                    f"💰 {r['price']}$ | ⏱ {r['duration']}\n\n"
                )

        await send_message(user_id, text)

        ack(task_id)

    except Exception as e:
        print("[WORKER ERROR]", e)
        fail(task_id)
