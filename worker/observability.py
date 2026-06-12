import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

METRICS = "stream:metrics"

def emit(metric, value, tags={}):
    r.xadd(METRICS, {
        "metric": metric,
        "value": value,
        "ts": time.time(),
        "tags": str(tags)
    })
