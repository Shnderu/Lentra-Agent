import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

SLA_ZSET = "zset:sla"

def register_task(task_id, priority=1, ttl=60):
    deadline = time.time() + ttl

    r.zadd(SLA_ZSET, {
        task_id: deadline
    })

    r.hset(f"task:{task_id}", mapping={
        "priority": priority,
        "deadline": deadline
    })


def get_urgent_tasks():
    now = time.time()
    return r.zrangebyscore(SLA_ZSET, 0, now)
EOFcat << 'EOF' > /opt/lentra/worker/sla_engine.py
import redis
import time
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "lentra-redis"),
                port=6379,
                decode_responses=True)

SLA_ZSET = "zset:sla"

def register_task(task_id, priority=1, ttl=60):
    deadline = time.time() + ttl

    r.zadd(SLA_ZSET, {
        task_id: deadline
    })

    r.hset(f"task:{task_id}", mapping={
        "priority": priority,
        "deadline": deadline
    })


def get_urgent_tasks():
    now = time.time()
    return r.zrangebyscore(SLA_ZSET, 0, now)
