import redis
import json
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"), decode_responses=True)

RETRY = "stream:rent:retry"

STREAMS = [
    "stream:rent:tasks:shard:0",
    "stream:rent:tasks:shard:1"
]

print("RETRY ORCHESTRATOR ACTIVE")

def route(task_id):
    import hashlib
    return STREAMS[int(hashlib.md5(task_id.encode()).hexdigest(), 16) % 2]

while True:
    try:
        items = r.xread({RETRY: "0-0"}, count=10, block=5000)

        if not items:
            continue

        for stream, entries in items:
            for msg_id, data in entries:
                retry = int(data.get("retry", 1))
                task_id = data.get("task_id")

                delay = min(2 ** retry, 60)
                time.sleep(delay)

                target = route(task_id)

                payload = json.loads(data.get("payload", "{}"))

                r.xadd(target, {
                    "task_id": task_id,
                    "retry": retry,
                    "type": payload.get("type"),
                    "payload": payload.get("payload"),
                    "status": "queued"
                })

                r.xack(RETRY, "retry-group", msg_id)

    except Exception as e:
        print("[RETRY ERROR]", str(e))
        time.sleep(2)
