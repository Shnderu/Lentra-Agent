import redis
import time


class ReinforcementOptimizer:
    """
    Simple reward-based optimizer (stub RL layer).
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def reward(self, task_type: str, score: float):
        self.r.lpush(f"rl:{task_type}:reward", score)
        self.r.ltrim(f"rl:{task_type}:reward", 0, 100)

    def avg_reward(self, task_type: str):
        values = self.r.lrange(f"rl:{task_type}:reward", 0, 100)
        if not values:
            return 0.0

        nums = [float(v) for v in values]
        return sum(nums) / len(nums)
