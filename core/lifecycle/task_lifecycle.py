from dataclasses import dataclass
from typing import Dict, Any, Optional, Callable
import time
import json

from core.queue.streams import STREAM_TASKS
from core.queue.streams import STREAM_DLQ, STREAM_RETRY

# -----------------------------
# TASK CONTEXT
# -----------------------------

@dataclass
class TaskContext:
    task_id: str
    task_type: str
    payload: Dict[str, Any]
    retry: int = 0
    status: str = "queued"
    ts: float = 0.0


# -----------------------------
# LIFECYCLE STATES
# -----------------------------

class TaskState:
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    RETRY = "retry"


# -----------------------------
# CORE ENGINE
# -----------------------------

class TaskLifecycleEngine:
    """
    AI-native orchestration layer:
    - normalizes incoming stream task
    - routes to handler
    - controls retry/failure
    - emits results
    """

    def __init__(self, redis_client, handler_registry: Dict[str, Callable]):
        self.r = redis_client
        self.handlers = handler_registry

    # -------------------------
    # ENTRY POINT
    # -------------------------

    def handle_raw(self, msg: Dict[str, str]) -> bool:
        task = self._normalize(msg)

        self._mark_processing(task)

        try:
            result = self._dispatch(task)

            self._mark_done(task, result)
            self._emit_result(task, result)

            return True

        except Exception as e:
            return self._handle_error(task, e)

    # -------------------------
    # NORMALIZATION
    # -------------------------

    def _normalize(self, msg: Dict[str, str]) -> TaskContext:
        payload = msg.get("payload", "{}")

        if isinstance(payload, str):
            payload = json.loads(payload)

        return TaskContext(
            task_id=msg.get("task_id"),
            task_type=msg.get("type"),
            payload=payload,
            retry=int(msg.get("retry", 0)),
            status=msg.get("status", TaskState.QUEUED),
            ts=float(msg.get("ts", time.time()))
        )

    # -------------------------
    # DISPATCH
    # -------------------------

    def _dispatch(self, task: TaskContext) -> Any:
        handler = self.handlers.get(task.task_type)

        if not handler:
            raise Exception(f"No handler for task type: {task.task_type}")

        return handler(task.payload)

    # -------------------------
    # SUCCESS PATH
    # -------------------------

    def _mark_processing(self, task: TaskContext):
        task.status = TaskState.PROCESSING

    def _mark_done(self, task: TaskContext, result: Any):
        task.status = TaskState.DONE

    def _emit_result(self, task: TaskContext, result: Any):
        self.r.xadd("stream:rent:results", {
            "task_id": task.task_id,
            "type": task.task_type,
            "result": json.dumps(result),
            "status": "done",
            "ts": str(time.time())
        })

    # -------------------------
    # ERROR HANDLING
    # -------------------------

    def _handle_error(self, task: TaskContext, error: Exception) -> bool:
        task.retry += 1
        task.status = TaskState.FAILED

        if task.retry < 3:
            self.r.xadd(STREAM_RETRY, {
                "task_id": task.task_id,
                "type": task.task_type,
                "payload": json.dumps(task.payload),
                "retry": str(task.retry),
                "status": "retry",
                "error": str(error),
                "ts": str(time.time())
            })
            return False

        self.r.xadd(STREAM_DLQ, {
            "task_id": task.task_id,
            "type": task.task_type,
            "payload": json.dumps(task.payload),
            "retry": str(task.retry),
            "status": "dlq",
            "error": str(error),
            "ts": str(time.time())
        })

        return False
