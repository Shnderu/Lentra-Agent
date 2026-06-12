import json
import time

from core.control.state_machine import TaskState
from core.reliability.dlq import DLQ_STREAM, MAX_RETRIES
from core.reliability.lock import RedisLock
from core.observability.spans import start_span, end_span


def process(task: dict, r):
    task_id = task["id"]

    lock = RedisLock(r)

    if not lock.acquire(task_id):
        return

    span = start_span(task.get("trace_id", "no-trace"), "process_task")

    try:
        retries = task.get("retries", 0)

        if retries >= MAX_RETRIES:
            task["state"] = "dead"
            r.xadd(DLQ_STREAM, {"data": json.dumps(task)})
            r.set(f"task:{task_id}", json.dumps(task))
            return

        task["state"] = TaskState.PROCESSING
        task["created_at"] = time.time()

        r.set(f"task:{task_id}", json.dumps(task))

        time.sleep(0.2)

        if task_id.endswith("0"):
            raise Exception("fail")

        task["state"] = TaskState.DONE
        r.set(f"task:{task_id}", json.dumps(task))

    except Exception:
        task["state"] = TaskState.RETRY
        task["retries"] = retries + 1

        r.set(f"task:{task_id}", json.dumps(task))
        r.xadd("stream:rent:tasks", {"data": json.dumps(task)})

    finally:
        end_span(span)
        lock.release(task_id)
