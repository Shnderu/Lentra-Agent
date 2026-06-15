from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime


@dataclass
class Notification:
    user_id: int
    type: str
    payload: Dict[str, Any]
    created_at: datetime
