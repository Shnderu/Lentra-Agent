import redis
import random
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

WORKERS_SET = "set:workers"

def register_worker(worker_id, cost=1.0):
    r.hset(f"worker:{worker_id}", mapping={
        "cost": cost,
        "load": 0
    })
    r.sadd(WORKERS_SET, worker_id)


def select_worker():
    workers = list(r.smembers(WORKERS_SET))

    scored = []
    for w in workers:
        meta = r.hgetall(f"worker:{w}")
        cost = float(meta.get("cost", 1))
        load = float(meta.get("load", 0))

        score = cost * (1 + load)
        scored.append((score, w))

    scored.sort()
    return scored[0][1]
