import os
import time

import bootstrap

from core.engine.postgres_queue import (
    claim_tasks,
    mark_done,
    mark_failed,
)

from core.handlers.route_search import process as route_process

WORKER_ID = os.getenv("WORKER_ID", "worker")
BATCH_SIZE = 5

print("[WORKER START]", WORKER_ID)


def process_task(task):
    task_type = task.get("task_type")

    if task_type == "route_search":
        return route_process(task)

    raise Exception(f"Unknown task type: {task_type}")


while True:
    tasks = claim_tasks(WORKER_ID, BATCH_SIZE)

    if not tasks:
        print("[idle]")
        time.sleep(2)
        continue

    for task in tasks:
        try:
            print(
                "[TASK]",
                task["id"],
                task["task_type"]
            )

            result = process_task(task)

            print(
                "[TASK DONE]",
                task["id"],
                result
            )

            mark_done(task["id"], WORKER_ID)

        except Exception as e:
            print("[TASK ERROR]", e)

            mark_failed(
                task["id"],
                WORKER_ID,
                str(e)
            )
