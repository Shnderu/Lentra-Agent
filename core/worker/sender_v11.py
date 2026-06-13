import asyncio
import os
import json
import psycopg2

from aiogram import Bot

from core.tasks.task_repository import TaskRepository

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")

bot = Bot(token=BOT_TOKEN)
repo = TaskRepository(DATABASE_URL)


async def send_loop():

    print(">>> SENDER V11 STARTED")

    while True:

        try:
            tasks = repo.claim_tasks(limit=10)

            for task_id, task_type, payload in tasks:

                try:
                    if isinstance(payload, str):
                        payload = json.loads(payload)

                    user_id = payload.get("user_id")

                    if not user_id:
                        raise Exception("Missing user_id")

                    # result хранится в payload или отдельно
                    message = payload.get("message", "done")

                    await bot.send_message(chat_id=user_id, text=str(message))

                    repo.mark_done(task_id, {"sent": True})

                except Exception as e:
                    repo.mark_failed(task_id, str(e))

        except Exception as e:
            print("[SENDER LOOP ERROR]", e)

        await asyncio.sleep(2)


async def main():
    try:
        await send_loop()
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
