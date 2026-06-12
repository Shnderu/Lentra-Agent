import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

def detect_anomalies():
    metrics = r.xrevrange("stream:metrics", count=20)

    errors = 0

    for _, m in metrics:
        if "error" in m.get("metric", ""):
            errors += 1

    return errors > 5


def auto_heal():
    if detect_anomalies():
        r.publish("ops:events", "restart_workers")
