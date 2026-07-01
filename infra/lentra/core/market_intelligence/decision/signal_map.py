from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass
class SignalMap:
    """
    Unified signal representation for Market Intelligence OS.

    This is NOT a new intelligence layer.
    This is a normalization/aggregation layer over existing outputs.
    """

    # Core pricing signals
    price: Optional[float] = None
    market_price: Optional[float] = None
    deviation_pct: Optional[float] = None

    # Risk / fraud signals
    risk_level: Optional[str] = None
    fraud_score: Optional[float] = None

    # Structure signals
    duplicates: Optional[int] = None

    # Intelligence signals
    confidence: Optional[float] = None

    # Area / expat signals (future-filled, optional)
    area_score: Optional[float] = None
    internet_score: Optional[float] = None
    noise_score: Optional[float] = None

    # Derived decision signals
    verdict: Optional[str] = None

    # Raw passthrough (for non-mapped signals)
    raw: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class SignalMapBuilder:
    """
    Builds unified signal map from Market Intelligence output context.
    """

    def build(self, context: Dict[str, Any]) -> SignalMap:
        ui = context.get("ui", {}) or {}
        api = context.get("api", {}) or {}
        meta = context.get("meta", {}) or {}

        return SignalMap(
            # pricing
            price=ui.get("price"),
            market_price=ui.get("market_price"),
            deviation_pct=ui.get("deviation_pct"),

            # risk
            risk_level=ui.get("risk_level"),
            fraud_score=api.get("signals", {}).get("fraud_score"),

            # structure
            duplicates=ui.get("duplicates"),

            # intelligence confidence
            confidence=meta.get("confidence"),

            # derived / decision
            verdict=ui.get("verdict"),

            # optional future area intelligence hooks
            area_score=api.get("scores", {}).get("area_score"),
            internet_score=api.get("scores", {}).get("internet_score"),
            noise_score=api.get("scores", {}).get("noise_score"),

            # raw passthrough for full extensibility
            raw={
                "ui": ui,
                "api": api,
                "meta": meta
            }
        )
