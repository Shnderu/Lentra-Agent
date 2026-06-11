import redis
import time

class Metrics:
    def __init__(self, redis_host="redis", redis_port=6379):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    def incr(self, key: str):
        self.r.incr(f"metric:{key}")

    def observe_latency(self, key: str, start: float):
        duration = time.time() - start
        self.r.lpush(f"metric:latency:{key}", duration)
        self.r.ltrim(f"metric:latency:{key}", 0, 500)
