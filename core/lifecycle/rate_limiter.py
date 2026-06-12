import time
import redis


class RateLimiter:
    """
    Simple token bucket per key (city/provider/etc).
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379, limit=5, window=60):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )
        self.limit = limit
        self.window = window

    def allow(self, key: str) -> bool:
        now = int(time.time())
        bucket = f"rl:{key}:{now // self.window}"

        count = self.r.incr(bucket)
        self.r.expire(bucket, self.window)

        return count <= self.limit
