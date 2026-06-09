import redis
import json
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "flyrum-redis"),
    port=6379,
    decode_responses=True
)


def set_state(user_id: int, state: str):
    print("[FSM SET STATE]", user_id, state)
    r.set(f"fsm:{user_id}:state", state)


def get_state(user_id: int):
    value = r.get(f"fsm:{user_id}:state")
    print("[FSM GET STATE]", user_id, value)
    return value or "idle"


def set_data(user_id: int, key: str, value):
    r.hset(f"fsm:{user_id}:data", key, json.dumps(value))


def get_data(user_id: int):
    raw = r.hgetall(f"fsm:{user_id}:data")
    return {k: json.loads(v) for k, v in raw.items()}


def clear(user_id: int):
    r.delete(f"fsm:{user_id}:state")
    r.delete(f"fsm:{user_id}:data")
