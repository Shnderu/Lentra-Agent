import redis
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

REGIONS = ["eu-west", "eu-east", "asia"]

def rebalance():
    loads = {}

    for region in REGIONS:
        meta = r.hgetall(f"region:{region}")
        load = float(meta.get("load", 0))
        capacity = float(meta.get("capacity", 1))
        loads[region] = load / capacity

    worst = max(loads, key=loads.get)
    best = min(loads, key=loads.get)

    if loads[worst] - loads[best] > 0.5:
        r.publish("cloud:rebalance", f"{worst}->{best}")
