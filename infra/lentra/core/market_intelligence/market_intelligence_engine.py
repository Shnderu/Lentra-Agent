from copy import deepcopy

from lentra.core.market_intelligence.normalization.listing_normalizer import ListingNormalizer
from lentra.core.market_intelligence.decision.ranking_engine import RankingEngine
from lentra.core.market_intelligence.verdict.verdict_engine import VerdictEngine
from lentra.core.market_intelligence.confidence.confidence_engine import ConfidenceEngine

from lentra.core.market_intelligence.risk.risk_engine import RiskEngine
from lentra.core.market_intelligence.area.area_engine import AreaEngine
from lentra.core.market_intelligence.pricing.market_truth_engine import compute_market_truth


class MarketIntelligenceEngine:

    def __init__(self):
        self.normalizer = ListingNormalizer()
        self.ranker = RankingEngine()
        self.verdict = VerdictEngine()
        self.confidence = ConfidenceEngine()

        self.risk_engine = RiskEngine()
        self.area_engine = AreaEngine()

    def analyze(self, listings: list):

        results = []

        for raw in listings:

            listing = deepcopy(raw)

            listing = self.normalizer.normalize(listing)

            truth = compute_market_truth(listing)
            listing["price_deviation"] = truth.get("deviation", 0.0)
            listing["market_verdict"] = truth.get("verdict", "unknown")

            # AREA FIX (CRITICAL)
            try:
                area_result = self.area_engine.score(listing.get("location", ""))

                # normalize dict → float
                if isinstance(area_result, dict):
                    listing["area_score"] = (
                        area_result.get("area_quality")
                        or area_result.get("score")
                        or area_result.get("value")
                        or 5.0
                    )
                else:
                    listing["area_score"] = float(area_result)

            except Exception:
                listing["area_score"] = 5.0

            try:
                risk_result = self.risk_engine.evaluate(listing)

                listing["risk"] = (
                    risk_result.get("risk")
                    if isinstance(risk_result, dict)
                    else float(risk_result)
                )
            except Exception:
                listing["risk"] = 0.5

            listing["score"] = self.ranker.score(listing, {})

            listing = self.verdict.run(listing)
            listing = self.confidence.run(listing)

            results.append(listing.copy())

        return results
