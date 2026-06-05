import os
import json
import redis

REDIS_HOST = os.getenv("REDIS_HOST", "flyrum_redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


def get(key: str):
    data = _client.get(key)
    if not data:
        return None
    return json.loads(data)


def set(key: str, value, ttl: int = 3600):
    _client.setex(key, ttl, json.dumps(value))
