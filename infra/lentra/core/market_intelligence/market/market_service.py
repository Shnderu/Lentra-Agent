from lentra.core.market_intelligence.pricing.market_truth_engine import (
    MarketTruthEngine
)

from lentra.core.market_intelligence.market.market_snapshot import (
    MarketSnapshot
)

from lentra.core.market_intelligence.history.price_history_repository import (
    PriceHistoryRepository
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

        self.history_repository = PriceHistoryRepository()


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
            city=city
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
            "sample_size",
            len(listings)
        )

        snapshot.outliers_detected = truth.get(
            "outliers_detected",
            truth.get(
                "outliers_removed",
                0
            )
        )

        snapshot.confidence = truth.get(
            "confidence",
            0.0
        )

        snapshot.market_health = truth.get(
            "market_health",
            "unknown"
        )

        snapshot.clean_listings = truth.get(
            "clean_listings",
            []
        )


        return {

            "city": city,

            "snapshot": snapshot.to_dict(),

            "market_truth": truth

        }
