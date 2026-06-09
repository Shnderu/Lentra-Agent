
import redis
import json

r = redis.Redis(host="redis", port=6379, decode_responses=True)


def set_state(user_id: int, state: str):
    r.set(f"fsm:{user_id}:state", state)


def get_state(user_id: int):
    return r.get(f"fsm:{user_id}:state") or "idle"


def set_data(user_id: int, key: str, value):
    r.hset(f"fsm:{user_id}:data", key, json.dumps(value))


def get_data(user_id: int):
    raw = r.hgetall(f"fsm:{user_id}:data")
    return {k: json.loads(v) for k, v in raw.items()}


def clear(user_id: int):
    r.delete(f"fsm:{user_id}:state")
    r.delete(f"fsm:{user_id}:data")
