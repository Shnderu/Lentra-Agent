import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

LEASE_ZSET = "zset:leases"
HANG_TIMEOUT = 45


def detect_hanging_tasks():
    now = time.time()

    stuck = r.zrangebyscore(LEASE_ZSET, 0, now)

    return stuck


def recover_task(task_id):
    meta = r.hgetall(f"lease:{task_id}")

    if not meta:
        return

    r.delete(f"lease:{task_id}")
    r.zrem(LEASE_ZSET, task_id)

    r.xadd("stream:wf:tasks", {
        "task_id": task_id,
        "status": "recovered"
    })


while True:
    stuck = detect_hanging_tasks()

    for task in stuck:
        recover_task(task)

    time.sleep(10)
