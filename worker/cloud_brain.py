import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

def analyze_system():
    metrics = r.xrevrange("stream:metrics", count=100)

    load = 0
    errors = 0

    for _, m in metrics:
        if m.get("metric") == "load":
            load += float(m.get("value", 0))
        if "error" in m.get("metric", ""):
            errors += 1

    return load, errors


def decide():
    load, errors = analyze_system()

    if errors > 10:
        return "emergency_scale_down"

    if load > 80:
        return "scale_out"

    if load < 20:
        return "consolidate"

    return "stable"
