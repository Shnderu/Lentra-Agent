class IdempotencyStore:
    """
    Minimal Redis-based idempotency guard.
    """

    def __init__(self, redis):
        self.r = redis
        self.prefix = "idem:"

    def seen(self, key: str) -> bool:
        return self.r.exists(self.prefix + key) == 1

    def mark(self, key: str):
        self.r.set(self.prefix + key, "1", ex=3600)
