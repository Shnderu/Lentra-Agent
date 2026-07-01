from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UIBlock:
    price: Optional[float]
    market_price: Optional[float]
    deviation_pct: Optional[float]
    risk_level: Optional[str]
    duplicates: int
    verdict: str


@dataclass
class APIBlock:
    normalized: Dict[str, Any]
    signals: Dict[str, Any]
    scores: Dict[str, Any]


@dataclass
class MarketIntelligenceOutputContract:
    """
    ЕДИНЫЙ ФИНАЛЬНЫЙ КОНТРАКТ ВЫХОДА СИСТЕМЫ

    Используется:
    - API response
    - Telegram bot rendering
    - UI cards
    """

    ui: UIBlock
    api: APIBlock

    # мета
    trace_id: Optional[str] = None
    source_count: int = 0
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ui": self.ui.__dict__,
            "api": self.api.__dict__,
            "meta": {
                "trace_id": self.trace_id,
                "source_count": self.source_count,
                "confidence": self.confidence,
            },
        }
