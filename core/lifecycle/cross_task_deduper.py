import redis
import hashlib


class CrossTaskDeduper:
    """
    Global deduplication across system (not per-worker).
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379, ttl=3600):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.ttl = ttl

    def _key(self, task: dict):
        raw = f"{task.get('type')}:{task.get('payload')}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def is_duplicate(self, task: dict) -> bool:
        key = self._key(task)
        return self.r.exists(f"dedup:{key}") == 1

    def mark(self, task: dict):
        key = self._key(task)
        self.r.setex(f"dedup:{key}", self.ttl, "1")
