from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


@dataclass
class Listing:
    id: str
    title: str
    price: float
    currency: str
    location: str
    source: str

    normalized_price: Optional[float] = None

    market_deviation: Optional[float] = None
    market_price: Optional[float] = None

    risk_score: Optional[int] = None
    risk_level: Optional[str] = None
    risk_flags: List[str] = field(default_factory=list)

    duplicates: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "currency": self.currency,
            "location": self.location,
            "source": self.source,
            "normalized_price": self.normalized_price,
            "market_deviation": self.market_deviation,
            "market_price": self.market_price,
            "risk_score": self.risk_score,
            "risk_level": self.risk_level,
            "risk_flags": self.risk_flags,
            "duplicates": self.duplicates,
        }
