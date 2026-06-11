class IdempotencyStore:
    def __init__(self, redis_client):
        self.redis = redis_client

    def seen(self, key: str) -> bool:
        return self.redis.get(f"idemp:{key}") is not None

    def mark(self, key: str):
        self.redis.set(f"idemp:{key}", "1", ex=86400)
