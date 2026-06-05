from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Task:
    id: Optional[int]
    task_type: str
    payload: Dict[str, Any]
    retries: int = 3
    status: str = "pending"
