import time
import redis


class IdempotencyGuard:
    """
    Simple Redis-based deduplication layer.
    Prevents duplicate processing of the same task_id.
    """

    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.r = redis_client
        self.ttl = ttl

    def _key(self, task_id: str) -> str:
        return f"idem:{task_id}"

    def is_processed(self, task_id: str) -> bool:
        return self.r.exists(self._key(task_id)) == 1

    def mark_processing(self, task_id: str):
        self.r.set(self._key(task_id), "processing", ex=self.ttl)

    def mark_done(self, task_id: str):
        self.r.set(self._key(task_id), "done", ex=self.ttl)

    def mark_failed(self, task_id: str):
        self.r.set(self._key(task_id), "failed", ex=self.ttl)
