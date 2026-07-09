from lentra.core.market_intelligence.pricing.market_truth_engine import (
    MarketTruthEngine
)

from lentra.core.market_intelligence.market.market_snapshot import (
    MarketSnapshot
)

from lentra.core.market_intelligence.history.price_history_repository import (
    PriceHistoryRepository
)

from lentra.core.market_intelligence.history.price_trend_analyzer import (
    PriceTrendAnalyzer
)

from lentra.core.market_intelligence.explanation.market_explanation_engine import (
    MarketExplanationEngine
)

from lentra.core.market_intelligence.history.segment_intelligence import (
    SegmentIntelligence
)

from lentra.core.market_intelligence.history.market_movement import (
    MarketMovementAnalyzer
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
    PriceHistoryRepository
        |
        v
    Price Intelligence
    """

    def __init__(
        self,
        history_repository=None
    ):

        self.truth_engine = MarketTruthEngine()

        self.history_repository = (
            history_repository
            if history_repository
            else PriceHistoryRepository()
        )

        self.trend_analyzer = PriceTrendAnalyzer()

        self.explanation_engine = MarketExplanationEngine()


        self.segment_intelligence = SegmentIntelligence()

        self.market_movement = MarketMovementAnalyzer()


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
            0
        )

        snapshot.outliers_detected = truth.get(
            "outliers_removed",
            0
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


        history = self.history_repository.get_city_history(
            city
        )


        prices = [
            item.get("price")
            for item in history
            if item.get("price") is not None
        ]


        price_intelligence = self.trend_analyzer.analyze(
            prices
        )


        segment_intelligence = self.segment_intelligence.analyze(
            history
        )


        market_movement = self.market_movement.analyze(
            history
        )


        market_explanation = self.explanation_engine.explain(
            truth,
            price_intelligence,
            segment_intelligence,
            market_movement
        )



        return {

            "city": city,

            "snapshot": snapshot.to_dict(),

            "market_truth": truth,

            "price_intelligence": price_intelligence,

            "segment_intelligence": segment_intelligence,

            "market_movement": market_movement,

            "market_explanation": market_explanation

        }
