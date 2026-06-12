import time
import redis


class DistributedLock:
    """
    Simple Redis-based distributed lock for multi-worker safety.
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379, ttl=30):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.ttl = ttl

    def acquire(self, key: str, owner: str) -> bool:
        return self.r.set(
            f"lock:{key}",
            owner,
            nx=True,
            ex=self.ttl
        )

    def release(self, key: str, owner: str):
        current = self.r.get(f"lock:{key}")
        if current == owner:
            self.r.delete(f"lock:{key}")

    def is_locked(self, key: str) -> bool:
        return self.r.exists(f"lock:{key}") == 1
