from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class MarketSnapshot:
    """
    Market Intelligence snapshot.

    Represents current state of rental market.
    """

    city: str = "da_nang"

    median_price: float | None = None

    mean_price: float | None = None

    q1: float | None = None

    q3: float | None = None


    sample_size: int = 0

    outliers_detected: int = 0


    confidence: float = 0.0


    price_min: float | None = None

    price_max: float | None = None


    market_health: str = "unknown"


    clean_listings: List[Dict[str, Any]] | None = None


    def to_dict(
        self
    ) -> Dict[str, Any]:

        return asdict(self)
