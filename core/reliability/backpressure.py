import redis


class BackpressureController:
    def __init__(self, redis_client: redis.Redis, limit: int = 1000):
        self.r = redis_client
        self.limit = limit

    def allowed(self) -> bool:
        try:
            length = self.r.xlen("stream:rent:tasks")
        except Exception:
            length = self.r.llen("stream:rent:tasks")

        return length < self.limit
