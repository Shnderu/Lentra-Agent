import asyncio
import json
import os
import traceback

from aiogram import Bot
from core.worker.task_queue_v14 import (
    claim_tasks,
    mark_success,
    mark_failure
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)


async def safe_send(user_id, text):
    try:
        await bot.send_message(user_id, text)
        return True, None
    except Exception as e:
        return False, str(e)


async def handle_task(task_id, payload, result):
    try:
        if isinstance(payload, str):
            payload = json.loads(payload)

        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("missing user_id")

        ok, err = await safe_send(user_id, str(result))

        if ok:
            mark_success(task_id)
        else:
            mark_failure(task_id, err)

    except Exception as e:
        mark_failure(task_id, str(e))


async def worker_loop():
    print(">>> V14 SAFE WORKER STARTED")

    while True:
        try:
            tasks = claim_tasks(limit=10)

            for task in tasks:
                task_id, payload, result, attempts = task
                await handle_task(task_id, payload, result)

        except Exception as e:
            print("[LOOP ERROR]", str(e))
            traceback.print_exc()

        await asyncio.sleep(2)


async def shutdown():
    try:
        await bot.session.close()
    except:
        pass


if __name__ == "__main__":
    try:
        asyncio.run(worker_loop())
    finally:
        asyncio.run(shutdown())
