from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class ListingDTO:
    id: str
    title: str
    price: float
    currency: str = "USD"
    city: str = ""
    location: dict = None
    source: str = "unknown"

    market_price: float = 0.0
    deviation_pct: float = 0.0
    risk_score: float = 0.0

    raw: Dict[str, Any] = None

    @staticmethod
    def from_raw(data: Any) -> "ListingDTO":
        """
        Strict normalization boundary.
        Accepts dict OR Listing-like object safely.
        """

        if data is None:
            raise ValueError("ListingDTO.from_raw: data is None")

        # support both dict and object safely
        get = data.get if isinstance(data, dict) else getattr

        def safe(key, default=None):
            try:
                return get(key, default)
            except Exception:
                return getattr(data, key, default)

        return ListingDTO(
            id=safe("id", ""),
            title=safe("title", ""),
            price=float(safe("price", 0) or 0),
            currency=safe("currency", "USD"),
            city=safe("city", ""),
            location=safe("location", {}) or {},
            source=safe("source", "unknown"),
            market_price=float(safe("market_price", 0) or 0),
            deviation_pct=float(safe("deviation_pct", 0) or 0),
            risk_score=float(safe("risk_score", 0) or 0),
            raw=data if isinstance(data, dict) else {}
        )
