from typing import TypedDict, Optional, Dict, Any


class LocationContract(TypedDict, total=False):
    segment: str
    micro_market: str


class MarketObjectContract(TypedDict, total=False):
    price: float
    market_price: float
    risk: float
    confidence: float

    location: LocationContract

    # enriched fields
    deviation: float
    verdict: str

    # engine outputs
    ranking_score: float
    attractiveness: float

    # raw passthrough
    features: Dict[str, Any]
    signals: Dict[str, Any]
