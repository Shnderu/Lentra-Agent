from typing import List, Dict, Any
from lentra.core.v2.models.listing import Listing


class MarketIntelligenceV2:
    """
    V2 Market Intelligence Layer

    Responsibilities:
    - compute market price bands
    - detect anomalies
    - enrich listings with deviation context
    """

    def build_context(self, listings: List[Listing], query: Dict[str, Any]) -> Dict[str, Any]:

        prices = [l.price for l in listings if l.price is not None]

        if not prices:
            return {
                "market_price": None,
                "min_price": None,
                "max_price": None,
                "median_price": None,
                "band_low": None,
                "band_high": None,
            }

        prices_sorted = sorted(prices)

        n = len(prices_sorted)

        median = prices_sorted[n // 2]
        min_price = prices_sorted[0]
        max_price = prices_sorted[-1]

        # simple band model (MVP)
        band_low = median * 0.85
        band_high = median * 1.15

        return {
            "market_price": float(median),
            "min_price": float(min_price),
            "max_price": float(max_price),
            "median_price": float(median),
            "band_low": float(band_low),
            "band_high": float(band_high),
            "city": query.get("city"),
            "type": query.get("type"),
            "budget": query.get("budget"),
        }


def estimate_market_price_v2(listings: List[Listing], query: Dict[str, Any]):
    return MarketIntelligenceV2().build_context(listings, query)
