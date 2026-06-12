import json
import time
import redis

from core.queue.streams import (
    STREAM_TASKS,
    STREAM_RESULTS,
    STREAM_DLQ,
    STREAM_RETRY,
)


class TaskEventBus:
    """
    Unified event emission layer for lifecycle engine.
    """

    def __init__(self, redis_host="lentra-redis", redis_port=6379):
        self.r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True
        )

    def emit_task(self, task_id: str, task_type: str, payload: dict):
        self.r.xadd(
            STREAM_TASKS,
            {
                "task_id": task_id,
                "type": task_type,
                "payload": json.dumps(payload),
                "status": "queued",
                "ts": time.time()
            }
        )

    def emit_result(self, task_id: str, result: dict):
        self.r.xadd(
            STREAM_RESULTS,
            {
                "task_id": task_id,
                "result": json.dumps(result),
                "ts": time.time()
            }
        )

    def emit_retry(self, task: dict):
        task["retry"] = int(task.get("retry", 0)) + 1

        self.r.xadd(
            STREAM_RETRY,
            {
                "task_id": task.get("task_id"),
                "task": json.dumps(task),
                "retry": task["retry"],
                "ts": time.time()
            }
        )

    def emit_dlq(self, task: dict, reason: str):
        self.r.xadd(
            STREAM_DLQ,
            {
                "task_id": task.get("task_id"),
                "task": json.dumps(task),
                "reason": reason,
                "ts": time.time()
            }
        )
