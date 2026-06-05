from core.redis import r
import json

def set_cache(key: str, value: dict, ttl: int = 300):
    r.setex(key, ttl, json.dumps(value))

def get_cache(key: str):
    data = r.get(key)
    return json.loads(data) if data else None
