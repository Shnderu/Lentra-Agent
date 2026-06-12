import redis


class FailurePredictor:
    """
    Predicts likely failure based on historical ratios.
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def risk_score(self, task_type: str) -> float:
        fail = int(self.r.get(f"perf:{task_type}:failure") or 0)
        success_len = len(self.r.lrange(f"perf:{task_type}:success", 0, 100))

        total = fail + success_len
        if total == 0:
            return 0.0

        return fail / total
