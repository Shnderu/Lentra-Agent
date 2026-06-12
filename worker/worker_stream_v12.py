import redis
import time
import json
import os

from core.queue.streams import STREAM_TASKS
from core.reliability.retry import RetryHandler

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

retry = RetryHandler(r)

GROUP = "workers"
CONSUMER = "worker-1"

try:
    r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
except:
    pass

print("STREAM WORKER V12 ACTIVE")


def process(task):
    # TODO: real business logic hook
    if task["type"] == "rent.search":
        return True
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
            for msg_id, data in entries:
                try:
                    print("[TASK]", data)

                    ok = process(data)

                    if ok:
                        r.xack(STREAM_TASKS, GROUP, msg_id)
                    else:
                        retry.schedule_retry(data)
                        r.xack(STREAM_TASKS, GROUP, msg_id)

                except Exception as e:
                    retry.schedule_retry(data)
                    r.xack(STREAM_TASKS, GROUP, msg_id)

    except Exception as e:
        print("[REDIS ERROR]", str(e))
        time.sleep(2)
