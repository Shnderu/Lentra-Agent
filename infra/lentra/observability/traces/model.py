# ============================================================
# LENTRA TRACE MODEL V16.8
# ============================================================

import time
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class TraceEvent:
    stage: str
    timestamp: float = field(default_factory=time.time)
    meta: Dict[str, Any] = None


@dataclass
class RequestTrace:
    request_id: str
    events: List[TraceEvent] = field(default_factory=list)

    def add(self, stage: str, meta=None):
        self.events.append(TraceEvent(stage=stage, meta=meta or {}))
