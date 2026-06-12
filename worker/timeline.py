import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

TIMELINE = "stream:timeline"

def emit_event(event):
    r.xadd(TIMELINE, {
        **event,
        "ts": time.time()
    })
