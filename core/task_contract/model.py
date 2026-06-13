from dataclasses import dataclass
from typing import Any, Dict, Optional
from datetime import datetime


@dataclass
class Task:
    id: int
    type: str
    payload: Dict[str, Any]
    status: str

    result: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
