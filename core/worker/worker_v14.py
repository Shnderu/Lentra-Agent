import asyncio
import json
import os

from aiogram import Bot

from core.worker.task_queue_v14 import (
    claim_tasks,
    mark_success,
    mark_failure
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)


async def handle(task_id, payload, result):
    if isinstance(payload, str):
        payload = json.loads(payload)

    user_id = payload["user_id"]

    await bot.send_message(user_id, str(result))
    mark_success(task_id)


async def loop():
    print(">>> WORKER V14 STARTED")

    while True:
        try:
            tasks = claim_tasks(limit=10)

            for task_id, payload, result, attempts in tasks:
                try:
                    await handle(task_id, payload, result)
                except Exception as e:
                    mark_failure(task_id, str(e))
                    print("[TASK FAIL]", task_id, e)

        except Exception as e:
            print("[WORKER LOOP FAIL]", e)

        await asyncio.sleep(2)


if __name__ == "__main__":
    asyncio.run(loop())
