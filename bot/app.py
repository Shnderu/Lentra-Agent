import os
import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

from core.engine.redis_queue import push_task, pop_result

logging.basicConfig(level=logging.INFO)

dp = Dispatcher()


def format_results(data):
    results = data.get("results", [])

    if not results:
        return "Рейсов не найдено"

    text = "✈️ Результаты:\n\n"

    for r in results:
        text += f"{r['from']} → {r['to']}\n{r['price']}$\n\n"

    return text


@dp.message(F.text == "/start")
async def start(m: Message):
    await m.answer("FlyRum AI ONLINE")


@dp.message()
async def handler(m: Message):
    task = {
        "id": str(m.message_id),
        "payload": {
            "text": m.text,
            "user_id": m.from_user.id
        }
    }

    push_task(json.dumps(task))
    await m.answer("Ищу билеты...")


async def result_loop(bot: Bot):
    print("RESULT LOOP STARTED")

    while True:
        raw = pop_result()

        if raw:
            try:
                res = json.loads(raw)

                await bot.send_message(
                    res["user_id"],
                    format_results(res["data"])
                )

            except Exception as e:
                logging.error(f"ERROR: {e}")

        await asyncio.sleep(1)


async def main():
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("BOT_TOKEN missing")

    bot = Bot(token=token)

    await asyncio.gather(
        dp.start_polling(bot),
        result_loop(bot)
    )


if __name__ == "__main__":
    asyncio.run(main())
