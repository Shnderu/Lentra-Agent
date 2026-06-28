from dataclasses import dataclass
from typing import Optional


@dataclass
class Listing:
    id: str
    title: str
    price: float
    currency: str
    city: str
    location: str
    source: str

    # enriched fields
    idempotency_key: Optional[str] = None
    cluster_id: Optional[str] = None
    normalized_price: Optional[float] = None
    risk_score: Optional[float] = None
    signal: Optional[str] = None
