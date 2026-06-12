import time
import redis


STREAM_TRACE = "stream:trace:tasks"


class TraceBus:
    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def span(self, task_id: str, stage: str, meta: dict):
        self.r.xadd(
            STREAM_TRACE,
            {
                "task_id": task_id,
                "stage": stage,
                "meta": str(meta),
                "ts": time.time()
            }
        )
