from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MarketEvent:
    type: str
    payload: Dict[str, Any]
