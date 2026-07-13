from lentra.core.market_intelligence.ranking.ranking_authority import (
    RankingAuthority
)

from lentra.core.market_intelligence.explanation.unified_explainer import (
    UnifiedExplainer
)

from lentra.core.market_intelligence.verdict.verdict_engine import (
    VerdictEngine
)

from lentra.core.market_intelligence.risk.market_risk_engine import (
    MarketRiskEngine
)


class AIDecisionEngine:
    """
    AI Decision Layer.

    Ranking is delegated through RankingAuthority.
    """

    def __init__(self):

        self.ranker = RankingAuthority()

        self.explainer = UnifiedExplainer()

        self.verdict = VerdictEngine()

        self.risk = MarketRiskEngine()


    def decide(
        self,
        payload: dict
    ):

        listings = payload.get(
            "listings",
            []
        )

        market_truth = payload.get(
            "market_truth",
            {}
        )

        enriched = []

        for listing in listings:

            scored = self.risk.score(
                listing
            )

            enriched.append(
                scored
            )

        ranked = self.ranker.rank(
            enriched,
            market_truth
        )

        final = []

        for item in ranked:

            item["verdict"] = self.verdict.evaluate(
                item,
                market_truth
            )

            item["explanation"] = self.explainer.explain(
                item
            )

            final.append(
                item
            )

        return {
            "ranked_listings": final,
            "summary": self._build_summary(
                final,
                market_truth
            )
        }


    def _build_summary(
        self,
        listings,
        market_truth
    ):

        best = listings[0] if listings else None

        return {
            "market_median": market_truth.get(
                "median_price"
            ),
            "best_deal": (
                best.get("price")
                if best
                else None
            ),
            "recommendation": (
                best.get("verdict")
                if best
                else None
            )
        }
