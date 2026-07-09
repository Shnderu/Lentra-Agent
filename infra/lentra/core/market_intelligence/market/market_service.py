from lentra.core.market_intelligence.pricing.market_truth_engine import (
    MarketTruthEngine
)

from lentra.core.market_intelligence.models.market_snapshot import (
    MarketSnapshot
)


class MarketService:
    """
    Market Intelligence market analysis service.

    Flow:

    listings
        |
        v
    MarketTruthEngine
        |
        v
    MarketSnapshot
        |
        v
    market context
    """

    def __init__(self):

        self.truth_engine = MarketTruthEngine()


    def analyze(
        self,
        listings: list,
        query: str = "",
        city: str = "da_nang"
    ) -> dict:

        truth = self.truth_engine.stabilize(
            listings
        )


        snapshot = MarketSnapshot(
            query=query
        )


        snapshot.median_price = truth.get(
            "median_price"
        )

        snapshot.mean_price = truth.get(
            "mean_price"
        )

        snapshot.q1 = truth.get(
            "q1"
        )

        snapshot.q3 = truth.get(
            "q3"
        )

        snapshot.price_min = truth.get(
            "price_min"
        )

        snapshot.price_max = truth.get(
            "price_max"
        )

        snapshot.sample_size = truth.get(
            "sample_size"
        )

        snapshot.outliers_detected = truth.get(
            "outliers_detected"
        )

        snapshot.confidence = truth.get(
            "confidence"
        )

        snapshot.market_health = truth.get(
            "market_health"
        )

        snapshot.total_objects = len(
            listings
        )


        return {

            "city": city,

            "snapshot": snapshot.finalize(),

            "market_truth": truth

        }
