import redis
import time

STREAM_TASKS = "stream:rent:tasks"
GROUP = "workers"


class StreamRecovery:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def recover_stuck(self, consumer: str, min_idle_ms: int = 60000):
        pending = self.r.xpending_range(
            STREAM_TASKS,
            GROUP,
            min="-",
            max="+",
            count=100
        )

        for item in pending:
            if item["idle"] > min_idle_ms:
                self.r.xclaim(
                    STREAM_TASKS,
                    GROUP,
                    consumer,
                    min_idle_ms,
                    item["message_id"]
                )
