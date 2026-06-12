import redis
import time
import uuid
import os
import random

r = redis.Redis(
    host=os.getenv("REDIS_HOST", "lentra-redis"),
    port=6379,
    decode_responses=True
)

AGENT_STREAM = "stream:agents:events"
MARKET_STREAM = "stream:market:bids"


class Agent:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.skill = random.uniform(0.5, 1.5)
        self.cost = random.uniform(0.1, 1.0)
        self.reputation = 1.0

    def bid(self, task_id):
        price = self.cost / self.skill * (1.0 / max(self.reputation, 0.1))

        r.xadd(MARKET_STREAM, {
            "agent_id": self.id,
            "task_id": task_id,
            "price": price,
            "ts": time.time()
        })

    def execute(self, task):
        success = random.random() < self.skill

        if success:
            self.reputation *= 1.01
        else:
            self.reputation *= 0.95

        r.xadd(AGENT_STREAM, {
            "agent_id": self.id,
            "result": "success" if success else "fail",
            "ts": time.time()
        })


def spawn_population(n=10):
    return [Agent() for _ in range(n)]
