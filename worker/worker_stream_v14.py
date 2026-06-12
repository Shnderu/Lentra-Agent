import redis
import os

from core.queue.streams import STREAM_TASKS
from core.lifecycle.task_lifecycle_v2 import TaskLifecycleEngineV2

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

GROUP = "workers"
CONSUMER = "worker-1"

engine = TaskLifecycleEngineV2()

try:
    r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
except:
    pass

print("AI-NATIVE ORCHESTRATION ENGINE ACTIVE (V14)")


while True:
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

                result = engine.process(data)

                if result.get("status") == "done":
                    r.xack(STREAM_TASKS, GROUP, msg_id)

            except Exception as e:
                print("[ERROR]", str(e))
                r.xack(STREAM_TASKS, GROUP, msg_id)
