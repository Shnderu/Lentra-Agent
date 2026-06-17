from dataclasses import dataclass
from typing import Any, Dict
import time
import uuid


@dataclass
class Event:
    type: str
    payload: Dict[str, Any]
    trace_id: str = None
    ts: float = None

    def __post_init__(self):
        if self.trace_id is None:
            self.trace_id = str(uuid.uuid4())
        if self.ts is None:
            self.ts = time.time()
