import time
from core.engine.queue import push_task

MAX_RETRIES = 3


def retry_task(task):
    retries = task.get("retries", 0) + 1

    if retries > MAX_RETRIES:
        print("[DLQ] dropped:", task["id"])
        return

    time.sleep(2 ** retries)

    task["retries"] = retries
    push_task(task["type"], task["payload"], priority=10)
