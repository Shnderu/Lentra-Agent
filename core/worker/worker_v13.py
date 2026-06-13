import asyncio
import json
import os

from aiogram import Bot
from core.worker.task_queue_v13 import (
    claim_tasks,
    mark_done,
    mark_failed
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)


async def process_task(task_id, payload, result):
    if isinstance(payload, str):
        payload = json.loads(payload)

    user_id = payload["user_id"]

    await bot.send_message(user_id, str(result))
    mark_done(task_id)


async def worker_loop():
    print(">>> WORKER V13 STARTED")

    while True:
        try:
            tasks = claim_tasks(limit=10)

            for task_id, payload, result in tasks:
                try:
                    await process_task(task_id, payload, result)
                except Exception as e:
                    mark_failed(task_id, str(e))
                    print("[TASK ERROR]", task_id, e)

        except Exception as e:
            print("[WORKER LOOP ERROR]", e)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(worker_loop())
