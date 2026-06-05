import redis
import json
import os

r = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, decode_responses=True)

def push_task(task_type, payload, priority=5):
    key = f"queue:{priority}"
    r.lpush(key, json.dumps({
        "type": task_type,
        "payload": payload
    }))

def pop_task():
    for priority in range(10, 0, -1):
        key = f"queue:{priority}"
        task = r.rpop(key)
        if task:
            return json.loads(task)
    return None
