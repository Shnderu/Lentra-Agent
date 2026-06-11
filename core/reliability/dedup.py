import redis
import hashlib
import json


class Deduplicator:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def fingerprint(self, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()

    def is_duplicate(self, fp: str, ttl: int = 3600) -> bool:
        key = f"dedup:{fp}"
        return not self.r.set(key, "1", nx=True, ex=ttl)
