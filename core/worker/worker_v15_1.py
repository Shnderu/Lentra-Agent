import asyncio
import json
import os
import traceback

from aiogram import Bot

from core.worker.router import TaskRouter
from core.worker.task_queue_v14_safe import (
    claim_tasks,
    mark_success,
    mark_failure
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


router = TaskRouter()
bot = Bot(token=BOT_TOKEN)


def normalize_task(row):
    task_id, payload, result, attempts = row

    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except Exception:
            payload = {}

    return {
        "id": task_id,
        "type": payload.get("type", "send_message"),
        "payload": payload,
        "result": result,
        "attempts": attempts
    }


async def process_task(task_row):
    task = normalize_task(task_row)

    try:
        result = await router.route(task)

        mark_success(task["id"])
        return result

    except Exception as e:
        mark_failure(task["id"], str(e))
        return None


async def worker_loop():
    print(">>> V15.1 ROUTER WORKER STARTED")

    while True:
        try:
            rows = claim_tasks(limit=10)

            for row in rows:
                await process_task(row)

        except Exception as e:
            print("[WORKER LOOP ERROR]", str(e))
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
