from dataclasses import dataclass
from typing import Any, Dict
import time


@dataclass
class VisibilityEvent:
    type: str
    payload: Dict[str, Any]
    ts: float = None

    def __post_init__(self):
        if self.ts is None:
            self.ts = time.time()
