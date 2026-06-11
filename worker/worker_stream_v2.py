import redis
import time
import json

from core.reliability.recovery_v2 import RecoveryV2
from core.reliability.dlq_v2 import DLQV2
from core.reliability.retry_policy import RetryPolicy

STREAM = "stream:rent:tasks"
GROUP = "workers"

r = redis.Redis(host="redis", port=6379, decode_responses=True)

try:
    r.xgroup_create(STREAM, GROUP, mkstream=True)
except Exception:
    pass

recovery = RecoveryV2(r)
dlq = DLQV2(r)
retry = RetryPolicy()


def process(task):
    time.sleep(0.05)
    return True


while True:
    recovery.reclaim_stuck("worker-1")

    resp = r.xreadgroup(GROUP, "worker-1", {STREAM: ">"}, count=10, block=5000)

    if not resp:
        continue

    for _, messages in resp:
        for msg_id, data in messages:
            try:
                process(data)
                r.xack(STREAM, GROUP, msg_id)

            except Exception as e:
                attempt = int(data.get("retry", 0))
                delay = retry.get_delay(attempt)

                dlq.push(data["task_id"], data, str(e))
                r.xack(STREAM, GROUP, msg_id)

                time.sleep(delay)
