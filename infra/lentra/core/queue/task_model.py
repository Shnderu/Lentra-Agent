from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class Task:
    id: str
    payload: Dict[str, Any]
    status: str
