import time
import redis

r = redis.Redis(host="lentra-redis", port=6379, decode_responses=True)

STREAM_TASKS = "stream:rent:tasks"
STREAM_RESULTS = "stream:rent:results"


def health_snapshot():
    tasks = len(r.xrange(STREAM_TASKS, "-", "+"))
    results = len(r.xrange(STREAM_RESULTS, "-", "+"))

    lag = tasks - results

    snapshot = {
        "ts": time.time(),
        "tasks": tasks,
        "results": results,
        "lag": lag,
        "status": "DEGRADED" if lag > 10 else "OK"
    }

    return snapshot


if __name__ == "__main__":
    import json
    print(json.dumps(health_snapshot(), indent=2))
