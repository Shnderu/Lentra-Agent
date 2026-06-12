import redis
import os
import time

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

WF_STREAM = "stream:wf:tasks"
RENT_STREAM = "stream:rent:tasks"

print("STREAM BRIDGE (REDIS ONLY) ACTIVE")

while True:
    try:
        events = r.xread({WF_STREAM: ">"}, block=5000, count=10)

        if not events:
            continue

        for stream, messages in events:
            for msg_id, data in messages:
                r.xadd(RENT_STREAM, data)
                print("[BRIDGE]", msg_id)

    except Exception as e:
        print("[BRIDGE ERROR]", str(e))
        time.sleep(2)
