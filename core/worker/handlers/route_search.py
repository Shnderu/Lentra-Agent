from core.queue.queue import ack, fail
from core.flight_engine.engine_impl import FlightEngineImpl
from core.bot.client import send_message

engine = FlightEngineImpl()


async def handle(task: dict):

    task_id = task["id"]
    payload = task["payload"]

    user_id = payload["user_id"]

    try:
        results = await engine.search(
            payload["origin"],
            payload["destination"],
            payload["date"]
        )

        text = "✈️ Результаты поиска\n\n"

        for r in results:
            text += (
                f"{r['airline']}\n"
                f"{r['from']} → {r['to']}\n"
                f"💰 {r['price']}$ | ⏱ {r['duration']}\n\n"
            )

        await send_message(user_id, text)

        ack(task_id)

    except Exception as e:
        print("[WORKER ERROR]", e)
        fail(task_id)
