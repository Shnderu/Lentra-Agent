import time
import redis


class AdaptiveOptimizer:
    """
    Learns from task outcomes to adjust routing/cost/retry strategy.
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def record_success(self, task_type: str, latency: float):
        key = f"perf:{task_type}:success"
        self.r.lpush(key, latency)
        self.r.ltrim(key, 0, 100)

    def record_failure(self, task_type: str):
        key = f"perf:{task_type}:failure"
        self.r.incr(key)

    def avg_latency(self, task_type: str):
        key = f"perf:{task_type}:success"
        values = self.r.lrange(key, 0, 100)

        if not values:
            return None

        nums = [float(v) for v in values]
        return sum(nums) / len(nums)

    def failure_rate(self, task_type: str):
        fail_key = f"perf:{task_type}:failure"
        fail = int(self.r.get(fail_key) or 0)

        success = len(self.r.lrange(f"perf:{task_type}:success", 0, 100))

        total = success + fail
        if total == 0:
            return 0.0

        return fail / total
