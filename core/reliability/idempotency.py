import redis

class IdempotencyGuard:
    def __init__(self, r):
        self.r = r

    def acquire(self, key: str) -> bool:
        return self.r.set(f"idem:{key}", "1", nx=True, ex=3600)
