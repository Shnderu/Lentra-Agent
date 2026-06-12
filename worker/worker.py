import redis
import time
import os

STREAM_TASKS = "stream:rent:tasks"

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

GROUP = "workers"
CONSUMER = "worker-1"

try:
    r.xgroup_create(STREAM_TASKS, GROUP, id="0", mkstream=True)
except:
    pass

print("STREAM WORKER ACTIVE (FIXED)")


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
                print("[TASK]", data)
                r.xack(STREAM_TASKS, GROUP, msg_id)

    except Exception as e:
        print("[ERROR]", str(e))
        time.sleep(2)
