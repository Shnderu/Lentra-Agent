class Metrics:
    def __init__(self, redis_client):
        self.r = redis_client

    def inc(self, key: str):
        self.r.incr(f"metrics:{key}")

    def get(self, key: str):
        return int(self.r.get(f"metrics:{key}") or 0)
