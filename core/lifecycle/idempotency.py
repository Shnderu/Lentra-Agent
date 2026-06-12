import time
import redis


class Idempotency:
    """
    Prevent duplicate task execution.
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379, ttl=3600):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.ttl = ttl

    def seen(self, key: str) -> bool:
        return self.r.exists(f"idem:{key}") == 1

    def mark(self, key: str):
        self.r.setex(f"idem:{key}", self.ttl, str(time.time()))
