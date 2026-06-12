import redis
import time
import uuid
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

LEASE_ZSET = "zset:leases"
LEASE_TTL = 30

def acquire_lease(task_id, worker_id):
    now = time.time()

    current = r.zscore(LEASE_ZSET, task_id)

    if current and current > now:
        return False

    r.zadd(LEASE_ZSET, {task_id: now + LEASE_TTL})

    r.hset(f"lease:{task_id}", mapping={
        "worker": worker_id,
        "ts": now
    })

    return True


def heartbeat(task_id):
    r.zadd(LEASE_ZSET, {task_id: time.time() + LEASE_TTL})


def release(task_id):
    r.zrem(LEASE_ZSET, task_id)
    r.delete(f"lease:{task_id}")
