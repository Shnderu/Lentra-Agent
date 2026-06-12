import redis
import os
import time
import json

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

EVENT_STREAM = "stream:events"
TASK_STREAM = "stream:wf:tasks"

GROUP = "event-workers"
CONSUMER = "e1"

try:
    r.xgroup_create(EVENT_STREAM, GROUP, id="0", mkstream=True)
except:
    pass


def publish_event(event_type, data):
    r.xadd(EVENT_STREAM, {"type": event_type, **data})


while True:
    resp = r.xreadgroup(GROUP, CONSUMER, {EVENT_STREAM: ">"}, count=10, block=5000)

    if not resp:
        continue

    for stream, entries in resp:
        for msg_id, data in entries:

            wf_id = data.get("wf_id")

            if data["type"] == "workflow_started":
                r.hset(f"wf:run:{wf_id}", "status", "running")

            if data["type"] == "step_completed":
                next_step = data.get("next_step")

                if next_step:
                    r.xadd(TASK_STREAM, {
                        "wf_id": wf_id,
                        "step": next_step
                    })

            r.xack(EVENT_STREAM, GROUP, msg_id)
