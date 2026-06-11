import redis
import json
import time

from core.queue.streams import STREAM_TASKS
from core.reliability.recovery import StreamRecovery

r = redis.Redis(host="redis", port=6379, decode_responses=True)

GROUP = "workers"
CONSUMER = "worker-1"

try:
    r.xgroup_create(STREAM_TASKS, GROUP, mkstream=True)
except Exception:
    pass

recovery = StreamRecovery(r)


def process(task):
    time.sleep(0.1)
    return True


while True:
    recovery.recover_stuck(CONSUMER)

    resp = r.xreadgroup(GROUP, CONSUMER, {STREAM_TASKS: ">"}, count=10, block=5000)

    if not resp:
        continue

    for _, messages in resp:
        for msg_id, data in messages:
            try:
                process(data)
                r.xack(STREAM_TASKS, GROUP, msg_id)

            except Exception:
                r.xadd("stream:rent:dlq", data)
                r.xack(STREAM_TASKS, GROUP, msg_id)
