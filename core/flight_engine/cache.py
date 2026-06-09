import redis
import json
import os

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "flyrum-redis"),
    port=6379,
    decode_responses=True
)


def get_cache(key: str):
    value = r.get(key)
    return json.loads(value) if value else None


def set_cache(key: str, value: dict, ttl: int = 300):
    r.set(key, json.dumps(value), ex=ttl)
