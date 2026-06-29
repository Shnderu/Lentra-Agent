from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MarketObject:
    price: float
    location: Dict[str, Any]

    risk: float
    confidence: float

    market_price: float = 0.0
    deviation: float = 0.0

    segment: str = "unknown"
    micro_market: str = "unknown"

    features: Dict[str, Any] = None
    signals: Dict[str, Any] = None
