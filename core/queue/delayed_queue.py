import time
import redis
import json

class DelayedQueue:
    """
    Simple delayed queue using sorted set:
    score = execution timestamp
    """

    def __init__(self, redis_host="redis", redis_port=6379):
        self.r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
        self.key = "delayed:rent:tasks"
        self.ready = "queue:rent:tasks"

    def schedule(self, task_id: str, delay_seconds: int):
        run_at = time.time() + delay_seconds
        self.r.zadd(self.key, {task_id: run_at})

    def tick(self):
        now = time.time()

        tasks = self.r.zrangebyscore(self.key, 0, now)

        for task_id in tasks:
            self.r.zrem(self.key, task_id)
            self.r.lpush(self.ready, task_id)
