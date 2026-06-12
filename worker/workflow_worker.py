import redis
import os
import time
import json
import uuid
from lease_manager import acquire_lease, heartbeat, release

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

STREAM = "stream:wf:tasks"
EVENTS = "stream:events"

GROUP = "wf-workers"
CONSUMER = "w1"

try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except:
    pass


def execute(step, payload):
    return {
        "result": f"processed:{step}",
        "meta": {"version": "v15"}
    }


while True:
    resp = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=5000)

    if not resp:
        continue

    for stream, entries in resp:
        for msg_id, data in entries:

            wf_id = data["wf_id"]
            step = data["step"]
            task_id = f"{wf_id}:{step}"

            try:
                if not acquire_lease(task_id, CONSUMER):
                    r.xack(STREAM, GROUP, msg_id)
                    continue

                heartbeat(task_id)

                result = execute(step, data)

                r.xadd(EVENTS, {
                    "type": "step_completed",
                    "wf_id": wf_id,
                    "step": step,
                    "result": json.dumps(result)
                })

                release(task_id)
                r.xack(STREAM, GROUP, msg_id)

            except Exception as e:
                r.xadd(EVENTS, {
                    "type": "step_failed",
                    "wf_id": wf_id,
                    "step": step,
                    "error": str(e)
                })

                release(task_id)
                r.xack(STREAM, GROUP, msg_id)
