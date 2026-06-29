from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class MarketContext:
    location: Optional[str]
    avg_price: Optional[int]
    risk_level: Optional[str]


class MarketContextBuilder:
    """
    Stub v0.1 — later will connect to:
    - listings DB
    - dedup engine
    - price aggregation layer
    """

    def build(self, property_obj: Dict[str, Any]) -> MarketContext:
        location = property_obj.get("location")

        # TEMP heuristics (replace later with real aggregation)
        if location == "da nang":
            avg_price = 550
        else:
            avg_price = 700

        return MarketContext(
            location=location,
            avg_price=avg_price,
            risk_level="unknown"
        )


market_context_builder = MarketContextBuilder()
