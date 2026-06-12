import redis
import os
import random

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

REGIONS = ["eu-west", "eu-east"]

def register_region(region, capacity=1.0):
    r.hset(f"region:{region}", mapping={
        "capacity": capacity,
        "load": 0
    })


def select_region():
    best = None
    best_score = float("inf")

    for region in REGIONS:
        meta = r.hgetall(f"region:{region}")

        cap = float(meta.get("capacity", 1))
        load = float(meta.get("load", 0))

        score = load / cap

        if score < best_score:
            best_score = score
            best = region

    return best or random.choice(REGIONS)
