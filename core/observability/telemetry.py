import time
import json
import traceback
from datetime import datetime


class Telemetry:
    def __init__(self, redis_client):
        self.r = redis_client

    def emit(self, event: dict):
        event["ts"] = time.time()
        self.r.xadd("stream:telemetry", event)

    def wrap_task(self, task_id: str, stage: str):
        return TaskContext(self, task_id, stage)


class TaskContext:
    def __init__(self, telemetry: Telemetry, task_id: str, stage: str):
        self.t = telemetry
        self.task_id = task_id
        self.stage = stage
        self.start = time.time()

    def success(self, extra=None):
        self.t.emit({
            "type": "task.success",
            "task_id": self.task_id,
            "stage": self.stage,
            "latency_ms": int((time.time() - self.start) * 1000),
            "extra": json.dumps(extra or {})
        })

    def error(self, e: Exception):
        self.t.emit({
            "type": "task.error",
            "task_id": self.task_id,
            "stage": self.stage,
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "stack": traceback.format_exc()
        })
