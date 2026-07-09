from dataclasses import dataclass, asdict
from typing import Any, Dict, List


@dataclass
class MarketSnapshot:
    """
    Represents calculated market state.

    This is the foundation object for
    Market Intelligence Layer.
    """

    city: str = "da_nang"

    median_price: float | None = None
    mean_price: float | None = None

    q1: float | None = None
    q3: float | None = None

    sample_size: int = 0

    outliers_detected: int = 0

    confidence: float = 0.0

    clean_listings: List[Dict[str, Any]] | None = None


    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
