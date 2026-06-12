from redis import Redis
import time


class IdempotencyGuard:
    """
    V7 CONTRACT:
    - acquire() = lock request (idempotent gate)
    - release() = optional cleanup
    """

    def __init__(self, redis_client: Redis, ttl: int = 3600):
        self.r = redis_client
        self.ttl = ttl

    def acquire(self, key: str) -> bool:
        """
        Returns:
            True  -> first time (allowed)
            False -> duplicate (blocked)
        """
        redis_key = f"idem:{key}"

        # SET NX = atomic lock
        result = self.r.set(redis_key, "1", nx=True, ex=self.ttl)

        return result is True

    def release(self, key: str):
        self.r.delete(f"idem:{key}")


class IdempotencyStore:
    """
    backward compatibility layer (if other modules still use old API)
    """

    def __init__(self, redis_client: Redis, ttl: int = 3600):
        self.r = redis_client
        self.ttl = ttl

    def seen(self, key: str) -> bool:
        return self.r.exists(f"idem:{key}") == 1

    def save(self, key: str):
        self.r.setex(f"idem:{key}", self.ttl, "1")
