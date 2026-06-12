import time
import json
import redis


class TaskTracer:
    """
    Minimal observability layer for task execution.
    Writes step-level events into Redis stream.
    """

    def __init__(self, redis_client: redis.Redis):
        self.r = redis_client

    def event(self, task_id: str, stage: str, meta: dict = None):
        payload = {
            "task_id": task_id,
            "stage": stage,
            "meta": json.dumps(meta or {}),
            "ts": time.time()
        }

        self.r.xadd("stream:rent:trace", payload)

    def start(self, task_id: str):
        self.event(task_id, "start")

    def processing(self, task_id: str):
        self.event(task_id, "processing")

    def success(self, task_id: str):
        self.event(task_id, "success")

    def failed(self, task_id: str, error: str):
        self.event(task_id, "failed", {"error": error})
