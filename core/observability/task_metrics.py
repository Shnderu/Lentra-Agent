import time
import redis


STREAM_METRICS = "stream:metrics:tasks"


class TaskMetrics:
    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def emit(self, task_id: str, status: str, task_type: str):
        self.r.xadd(
            STREAM_METRICS,
            {
                "task_id": task_id,
                "status": status,
                "type": task_type,
                "ts": time.time()
            }
        )
