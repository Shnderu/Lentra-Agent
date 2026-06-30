from lentra.core.market_intelligence.ranking.unified_ranking_engine import UnifiedRankingEngine
from lentra.core.market_intelligence.explanation.unified_explainer import UnifiedExplainer
from lentra.core.market_intelligence.verdict.verdict_engine import VerdictEngine
from lentra.core.market_intelligence.risk.market_risk_engine import MarketRiskEngine


class AIDecisionEngine:

    def __init__(self):
        self.ranker = UnifiedRankingEngine()
        self.explainer = UnifiedExplainer()
        self.verdict = VerdictEngine()
        self.risk = MarketRiskEngine()

    def decide(self, payload: dict):

        listings = payload.get("listings", [])
        market_truth = payload.get("market_truth", {})

        enriched = []

        # STEP 1: risk scoring
        for l in listings:
            l = self.risk.score(l)
            enriched.append(l)

        # STEP 2: ranking
        ranked = self.ranker.rank(enriched, market_truth)

        # STEP 3: verdict + explanation
        final = []

        for item in ranked:

            v = self.verdict.evaluate(item, market_truth)

            explanation = self.explainer.explain(
                item=item,
                verdict=v,
                market_truth=market_truth
            )

            item["verdict"] = v
            item["explanation"] = explanation

            final.append(item)

        return {
            "ranked_listings": final,
            "summary": self._build_summary(final, market_truth)
        }

    def _build_summary(self, listings, market_truth):

        best = listings[0] if listings else None

        return {
            "market_median": market_truth.get("median_price"),
            "best_deal": best.get("price") if best else None,
            "recommendation": best.get("verdict") if best else None
        }
