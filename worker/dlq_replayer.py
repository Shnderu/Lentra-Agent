import time
import json
import redis

from core.queue.streams import STREAM_DLQ, STREAM_TASKS
from core.lifecycle.task_store import TaskStore
from core.lifecycle.task_events import TaskEventBus
from core.lifecycle.task_lifecycle import TaskStatus


r = redis.Redis(
    host="lentra-redis",
    port=6379,
    decode_responses=True
)

store = TaskStore()
events = TaskEventBus()

GROUP = "dlq-replayer"
CONSUMER = "dlq-replayer-1"


try:
    r.xgroup_create(STREAM_DLQ, GROUP, id="0", mkstream=True)
except Exception:
    pass


print("DLQ REPLAYER ACTIVE")


def replay(task: dict):
    task_id = task.get("task_id")

    store.update_status(task_id, TaskStatus.QUEUED)

    r.xadd(
        STREAM_TASKS,
        {
            "task_id": task_id,
            "type": task.get("type"),
            "payload": task.get("payload"),
            "retry": 0,
            "status": "queued",
            "ts": time.time()
        }
    )


while True:
    try:
        messages = r.xreadgroup(
            GROUP,
            CONSUMER,
            {STREAM_DLQ: ">"},
            count=10,
            block=5000
        )

        if not messages:
            continue

        for stream, entries in messages:
            for msg_id, task in entries:
                try:
                    replay(task)

                    r.xack(STREAM_DLQ, GROUP, msg_id)

                except Exception as e:
                    print("[DLQ REPLAY ERROR]", str(e))
                    time.sleep(1)

    except Exception as e:
        print("[DLQ WORKER ERROR]", str(e))
        time.sleep(2)
