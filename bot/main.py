import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from core.queue.queue import get_conn

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def create_task(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    payload = {
        "user_id": user_id,
        "origin": "Самара",
        "destination": "Париж",
        "date": "2026-07-17"
    }

    cur.execute("""
        INSERT INTO tasks (type, payload, status, run_after)
        VALUES (%s, %s, %s, NOW())
    """, (
        "route_search",
        json.dumps(payload),
        "queued"
    ))

    conn.commit()
    conn.close()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    create_task(message.from_user.id)

    await message.answer(
        "🔍 Ищу рейсы...\nСамара → Париж\nДата: 17.07.26\nTask ID: создан"
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
