from dataclasses import dataclass
from typing import Any, Dict
from datetime import datetime


@dataclass
class Event:
    type: str
    user_id: int
    payload: Dict[str, Any]
    timestamp: datetime
