import redis

STREAM = "stream:rent:tasks"
GROUP = "workers"


class RecoveryV2:
    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def reclaim_stuck(self, consumer: str, min_idle: int = 60000):
        pending = self.r.xpending_range(
            STREAM,
            GROUP,
            min="-",
            max="+",
            count=50
        )

        for p in pending:
            if p.get("idle", 0) > min_idle:
                self.r.xclaim(
                    STREAM,
                    GROUP,
                    consumer,
                    min_idle,
                    p["message_id"]
                )
