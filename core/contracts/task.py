from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional
from enum import Enum
import time
import uuid


class TaskStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class TaskType(str, Enum):
    RENT_SEARCH = "rent.search"


@dataclass
class Task:
    id: str
    type: TaskType
    payload: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    created_at: float = None
    updated_at: float = None

    @staticmethod
    def create(task_type: str, payload: Dict[str, Any]) -> "Task":
        now = time.time()
        return Task(
            id=str(uuid.uuid4()),
            type=TaskType(task_type),
            payload=payload,
            status=TaskStatus.PENDING,
            result=None,
            created_at=now,
            updated_at=now,
        )

    def mark_processing(self):
        self.status = TaskStatus.PROCESSING
        self.updated_at = time.time()

    def mark_done(self, result: Dict[str, Any]):
        self.status = TaskStatus.DONE
        self.result = result
        self.updated_at = time.time()

    def mark_failed(self, error: str):
        self.status = TaskStatus.FAILED
        self.result = {"error": error}
        self.updated_at = time.time()

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["type"] = self.type.value
        data["status"] = self.status.value
        return data
