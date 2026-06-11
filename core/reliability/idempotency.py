import time
import redis


class IdempotencyGuard:
    def __init__(self, redis_client: redis.Redis, ttl: int = 3600):
        self.r = redis_client
        self.ttl = ttl

    def acquire(self, task_id: str) -> bool:
        key = f"idem:task:{task_id}"
        return bool(self.r.set(key, "1", nx=True, ex=self.ttl))

    def mark_done(self, task_id: str) -> None:
        key = f"idem:task:{task_id}"
        self.r.set(key, "done", ex=self.ttl)

    def is_done(self, task_id: str) -> bool:
        return self.r.get(f"idem:task:{task_id}") == b"done"
