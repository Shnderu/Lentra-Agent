from dataclasses import dataclass
from typing import Any, Optional, Literal
from datetime import datetime


TaskStatus = Literal[
    "pending",
    "processing",
    "done",
    "sent",
    "failed"
]


@dataclass
class Task:
    id: int
    type: str
    payload: dict
    status: TaskStatus

    created_at: datetime
    updated_at: Optional[datetime]

    result: Optional[dict]
    error: Optional[str]

    attempts: int
