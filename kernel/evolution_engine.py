import redis
import os
import time

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)


def record_failure(service, error):
    r.xadd("stream:system:failures", {
        "service": service,
        "error": error,
        "ts": time.time()
    })


def evolve():
    failures = r.xrevrange("stream:system:failures", count=100)

    if len(failures) > 20:
        r.publish("system:evolution", "architecture_shift_required")
