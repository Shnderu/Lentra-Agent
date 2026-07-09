from lentra.core.market_intelligence.pricing.market_truth_engine import (
    MarketTruthEngine
)

from lentra.core.market_intelligence.pricing.market_snapshot import (
    MarketSnapshot
)


class MarketService:
    """
    Market Intelligence pricing service.

    Single entry point for market analysis.

    Pipeline:

    listings
        |
        v
    MarketTruthEngine
        |
        v
    MarketSnapshot
    """


    def __init__(self):

        self.truth_engine = MarketTruthEngine()


    def analyze(
        self,
        listings: list[dict]
    ) -> dict:

        truth = self.truth_engine.stabilize(
            listings
        )


        prices = [
            l.get("price")
            for l in truth.get(
                "clean_listings",
                []
            )
            if l.get("price")
        ]


        snapshot = MarketSnapshot(

            city=self._detect_city(
                listings
            ),

            median_price=truth.get(
                "median_price"
            ),

            mean_price=truth.get(
                "mean_price"
            ),

            q1=truth.get(
                "q1"
            ),

            q3=truth.get(
                "q3"
            ),

            price_min=min(prices)
            if prices
            else None,

            price_max=max(prices)
            if prices
            else None,

            sample_size=len(prices),

            outliers_detected=truth.get(
                "outliers_removed",
                0
            ),

            confidence=self._confidence(
                len(prices)
            ),

            market_health="stable",

            clean_listings=truth.get(
                "clean_listings",
                []
            )
        )


        return snapshot.to_dict()


    def _detect_city(
        self,
        listings: list[dict]
    ) -> str:

        for item in listings:

            city = item.get(
                "city"
            )

            if city:
                return city

        return "unknown"


    def _confidence(
        self,
        size: int
    ) -> float:

        if size >= 20:
            return 0.9

        if size >= 10:
            return 0.6

        if size >= 5:
            return 0.25

        if size > 0:
            return 0.15

        return 0.0
