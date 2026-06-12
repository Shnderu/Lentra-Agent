import time


class RedisLock:
    def __init__(self, redis_client):
        self.r = redis_client

    def acquire(self, key: str, ttl: int = 30) -> bool:
        return self.r.set(f"lock:{key}", "1", nx=True, ex=ttl)

    def release(self, key: str):
        self.r.delete(f"lock:{key}")
