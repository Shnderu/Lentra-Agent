import asyncio
import traceback

from aiogram import Bot

from core.worker.router import TaskRouter
from core.worker.task_contract_v15_2 import (
    validate_task,
    TaskContractError
)

from core.worker.task_queue_v14_safe import (
    claim_tasks,
    mark_success,
    mark_failure
)

import os

router = TaskRouter()
bot = Bot(token=os.getenv("BOT_TOKEN"))


def normalize_row(row):
    task_id, payload, result, attempts = row

    return task_id, "send_message", payload


async def process(row):
    task_id, task_type, payload = normalize_row(row)

    try:
        task = validate_task(task_id, task_type, payload)

        await router.route(task)

        mark_success(task["id"])

    except TaskContractError as e:
        mark_failure(task_id, f"contract_error: {str(e)}")

    except Exception as e:
        mark_failure(task_id, f"runtime_error: {str(e)}")
        traceback.print_exc()


async def loop():
    print(">>> V15.2 CONTRACT WORKER STARTED")

    while True:
        try:
            rows = claim_tasks(limit=10)

            for row in rows:
                await process(row)

        except Exception as e:
            print("[LOOP ERROR]", e)

        await asyncio.sleep(2)


async def shutdown():
    try:
        await bot.session.close()
    except:
        pass


if __name__ == "__main__":
    asyncio.run(loop())
