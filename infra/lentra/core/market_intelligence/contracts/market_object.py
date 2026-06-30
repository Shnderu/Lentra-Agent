from typing import TypedDict, Optional


class MarketObject(TypedDict, total=False):
    title: str
    price: float
    city: Optional[str]
    location: Optional[str]

    risk_score: float
    dedup_id: str
    geo_score: float
    expat_score: float
    rank_score: float
