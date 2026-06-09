
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class Intent:

    name: str
    confidence: float
    payload: Dict[str, Any]
    source: str  # message / callback / fsm
