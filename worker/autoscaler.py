import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

METRICS = "stream:metrics"


def get_load():
    data = r.xrevrange(METRICS, count=50)

    total = 0
    count = 0

    for _, event in data:
        if event.get("metric") == "task_throughput":
            total += float(event.get("value", 0))
            count += 1

    return total / count if count else 0


def scale_decision():
    load = get_load()

    if load > 80:
        return "scale_up"
    elif load < 20:
        return "scale_down"
    return "stable"
