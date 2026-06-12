import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)


def optimize_graph(wf_id):
    steps = r.hgetall(f"wf:{wf_id}:steps")

    # naive optimization: remove redundant steps
    optimized = {}

    seen = set()

    for k, v in steps.items():
        if v in seen:
            continue
        seen.add(v)
        optimized[k] = v

    r.set(f"wf:{wf_id}:optimized", str(optimized))

    return optimized
