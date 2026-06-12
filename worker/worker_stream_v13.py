import json
import time
import redis

from core.queue.streams import STREAM_TASKS
from core.lifecycle.task_lifecycle import TaskStatus, TaskLifecycle
from core.lifecycle.task_store import TaskStore
from core.lifecycle.task_events import TaskEventBus
from worker.handlers.rent_search import RentSearchHandler


r = redis.Redis(
    host="lentra-redis",
    port=6379,
    decode_responses=True
)

GROUP = "workers"
CONSUMER = "worker-stream-v13"

store = TaskStore()
events = TaskEventBus()
handler = RentSearchHandler()


try:
    r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
except Exception:
    pass


print("STREAM WORKER LIFECYCLE V13 ACTIVE")


def process(task: dict):
    task_id = task.get("task_id")
    task_type = task.get("type")

    # mark processing
    store.update_status(task_id, TaskStatus.PROCESSING)

    if task_type == "rent.search":
        payload = json.loads(task.get("payload") or "{}")

        result = handler.handle(payload)

        store.update_status(task_id, TaskStatus.DONE)
        events.emit_result(task_id, result)

        return True

    store.update_status(task_id, TaskStatus.FAILED)
    return True


while True:
    try:
        messages = r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM_TASKS: ">"},
            count=10,
            block=5000
        )

        if not messages:
            continue

        for stream, entries in messages:
            for msg_id, task in entries:
                try:
                    task_id = task.get("task_id")

                    # validate transition
                    TaskLifecycle.assert_transition(
                        task.get("status", "queued"),
                        "processing"
                    )

                    process(task)

                    r.xack(STREAM_TASKS, GROUP, msg_id)

                except Exception as e:
                    # retry path
                    store.update_status(task.get("task_id"), TaskStatus.RETRY)
                    events.emit_retry(task)

                    r.xack(STREAM_TASKS, GROUP, msg_id)

    except Exception as e:
        print("[WORKER ERROR]", str(e))
        time.sleep(2)
