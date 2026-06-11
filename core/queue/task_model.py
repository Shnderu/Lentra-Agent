from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    type: str
    payload: dict
    status: str = "pending"
    result: Optional[dict] = None
