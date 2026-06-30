from dataclasses import dataclass
from time import time
from typing import Any, Dict
from lentra.core.market_intelligence.visibility.event_types import EventType


@dataclass
class VisibilityEvent:
    type: EventType
    payload: Dict[str, Any]
    ts: float = time()
