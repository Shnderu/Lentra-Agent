import redis
import json
import time

from core.queue.streams import STREAM_TASKS, STREAM_DLQ
from core.reliability.idempotency import IdempotencyGuard

r = redis.Redis(host="redis", port=6379, decode_responses=True)
idem = IdempotencyGuard(r)

GROUP = "workers"
CONSUMER = "worker-1"

try:
    r.xgroup_create(STREAM_TASKS, GROUP, mkstream=True)
except Exception:
    pass


def process(task):
    time.sleep(0.1)
    return {"status": "done"}


while True:
    resp = r.xreadgroup(GROUP, CONSUMER, {STREAM_TASKS: ">"}, count=10, block=5000)

    if not resp:
        continue

    for stream, messages in resp:
        for msg_id, data in messages:
            task_id = data["task_id"]
            retry = int(data.get("retry", 0))

            try:
                if idem.is_done(task_id):
                    r.xack(STREAM_TASKS, GROUP, msg_id)
                    continue

                result = process(data)

                idem.mark_done(task_id)
                r.xack(STREAM_TASKS, GROUP, msg_id)

            except Exception as e:
                retry += 1

                if retry >= 5:
                    r.xadd(STREAM_DLQ, {
                        "task_id": task_id,
                        "error": str(e),
                        "payload": str(data)
                    })
                    r.xack(STREAM_TASKS, GROUP, msg_id)
                else:
                    r.xadd(STREAM_TASKS, {
                        "task_id": task_id,
                        "type": data.get("type"),
                        "payload": data.get("payload"),
                        "retry": retry
                    })
                    r.xack(STREAM_TASKS, GROUP, msg_id)
