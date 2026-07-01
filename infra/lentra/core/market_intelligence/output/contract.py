from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class MarketIntelligenceOutputContract:
    ui: Dict[str, Any]
    api: Dict[str, Any]
    meta: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class MarketIntelligenceUIBlock:
    price: float
    market_price: float
    deviation_pct: float
    risk_level: str
    duplicates: int
    verdict: str

    # NEW: area intelligence (exposed, not computed here)
    area: Optional[Dict[str, Any]] = None

    # NEW: explanation layer
    explanation: Optional[Dict[str, Any]] = None


@dataclass
class MarketIntelligenceAPIBlock:
    normalized: Dict[str, Any]
    signals: Dict[str, Any]
    scores: Dict[str, Any]

    # NEW: market dynamics exposure
    dynamics: Optional[Dict[str, Any]] = None


@dataclass
class MarketIntelligenceMeta:
    trace_id: str
    source_count: int
    confidence: float

    # NEW: breakdown visibility
    confidence_breakdown: Optional[Dict[str, float]] = None
