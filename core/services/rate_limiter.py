import time
import redis


class RateLimiter:
    def __init__(self):
        self.client = redis.Redis(
            host="redis",
            port=6379,
            decode_responses=True
        )
        self.limit = 5  # запросов
        self.window = 60  # секунд

    def allow(self, user_id: int) -> bool:
        key = f"rate:{user_id}"
        count = self.client.get(key)

        if not count:
            self.client.setex(key, self.window, 1)
            return True

        if int(count) >= self.limit:
            return False

        self.client.incr(key)
        return True


rate_limiter = RateLimiter()
