import json
import redis

client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

QUEUE = "results"


def push_result(task_id: str, user_id: int, data: dict):
    payload = {
        "task_id": task_id,
        "user_id": user_id,
        "data": data
    }

    client.lpush(QUEUE, json.dumps(payload))


def pop_result():
    return client.rpop(QUEUE)
