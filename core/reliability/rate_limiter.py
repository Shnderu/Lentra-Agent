import time


class RateLimiter:
    def __init__(self, redis_client, key="global:rate"):
        self.r = redis_client
        self.key = key

    def allow(self, limit: int = 10, window: int = 1) -> bool:
        now = int(time.time())

        pipe = self.r.pipeline()
        pipe.zremrangebyscore(self.key, 0, now - window)
        pipe.zcard(self.key)
        _, count = pipe.execute()

        if count >= limit:
            return False

        self.r.zadd(self.key, {str(time.time()): now})
        return True
