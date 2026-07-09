from dataclasses import dataclass, field
from typing import Any


@dataclass
class MarketSnapshot:
    """
    Statistical market truth snapshot.

    Represents normalized market conditions
    calculated from listings.
    """

    city: str | None = None

    median_price: float | None = None

    mean_price: float | None = None

    q1: float | None = None

    q3: float | None = None

    price_min: float | None = None

    price_max: float | None = None

    sample_size: int = 0

    outliers_detected: int = 0

    confidence: float = 0.0

    market_health: str = "unknown"

    clean_listings: list[dict[str, Any]] = field(
        default_factory=list
    )


    def to_dict(self) -> dict:
        return {
            "city": self.city,
            "median_price": self.median_price,
            "mean_price": self.mean_price,
            "q1": self.q1,
            "q3": self.q3,
            "price_min": self.price_min,
            "price_max": self.price_max,
            "sample_size": self.sample_size,
            "outliers_detected": self.outliers_detected,
            "confidence": self.confidence,
            "market_health": self.market_health,
            "clean_listings": self.clean_listings,
        }
