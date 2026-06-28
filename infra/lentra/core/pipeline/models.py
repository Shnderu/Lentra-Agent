from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Listing:
    id: str
    title: str
    price: float
    currency: str
    city: str
    location: str
    source: str
    raw_text: str = ""

    normalized_price: Optional[float] = None
    market_price: Optional[float] = None

    risk_score: Optional[float] = None
    duplicates: Optional[List[str]] = None


# HARD EXPORT GUARANTEE (fix import ambiguity)
__all__ = ["Listing"]
