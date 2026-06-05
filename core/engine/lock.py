import os
import redis

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)


def acquire_lock(task_id):
    return r.set(f"lock:{task_id}", "1", nx=True, ex=30)


def release_lock(task_id):
    r.delete(f"lock:{task_id}")
