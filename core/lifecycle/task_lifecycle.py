from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional
import time


class TaskStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"
    RETRY = "retry"
    DLQ = "dlq"


@dataclass
class TaskContext:
    task_id: str
    type: str
    payload: Dict[str, Any]
    retry: int = 0
    status: TaskStatus = TaskStatus.QUEUED
    ts: float = 0.0


class TaskLifecycleEngine:
    MAX_RETRIES = 3

    def to_processing(self, task: TaskContext) -> TaskContext:
        task.status = TaskStatus.PROCESSING
        task.ts = time.time()
        return task

    def to_done(self, task: TaskContext) -> TaskContext:
        task.status = TaskStatus.DONE
        task.ts = time.time()
        return task

    def to_failed(self, task: TaskContext, error: Optional[str] = None) -> TaskContext:
        if task.retry >= self.MAX_RETRIES:
            task.status = TaskStatus.DLQ
        else:
            task.status = TaskStatus.RETRY
            task.retry += 1

        task.ts = time.time()
        return task


__all__ = [
    "TaskLifecycleEngine",
    "TaskContext",
    "TaskStatus"
]
