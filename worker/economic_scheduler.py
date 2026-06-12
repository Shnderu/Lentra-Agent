import redis
import os
import time
import uuid

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

BID_STREAM = "stream:task:bids"
TASK_STREAM = "stream:tasks:econ"


def submit_task(task):
    task_id = str(uuid.uuid4())

    r.xadd(TASK_STREAM, {
        "task_id": task_id,
        "type": task["type"],
        "sla": task.get("sla", "normal"),
        "status": "open"
    })

    return task_id


def bid(worker_id, task_id, cost):
    r.xadd(BID_STREAM, {
        "worker": worker_id,
        "task_id": task_id,
        "cost": cost,
        "ts": time.time()
    })


def select_best_bid(task_id):
    bids = r.xrange(BID_STREAM)

    best = None
    best_cost = float("inf")

    for _, b in bids:
        if b.get("task_id") == task_id:
            cost = float(b.get("cost", 999999))
            if cost < best_cost:
                best_cost = cost
                best = b

    return best
