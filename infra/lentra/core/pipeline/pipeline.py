from lentra.core.parsing.query_parser import parse_query
from lentra.core.data.fetcher import fetch_listings
from lentra.core.normalization.normalizer import normalize
from lentra.core.dedup.deduplicator import deduplicate

from lentra.core.market.pricing import estimate_market_price
from lentra.core.risk.risk_scorer import score_risk

from lentra.core.v2.market.market_intelligence import MarketIntelligenceV2
from lentra.core.v2.risk.risk_engine import RiskEngineV2
from lentra.core.v2.ranking.ranker_v2 import RankerV2
from lentra.core.v2.area.expat_area_score import ExpatAreaScoreV2
from lentra.core.v2.scoring.unified_scorer import UnifiedScorerV2
from lentra.core.v2.response.ux_builder import UXBuilderV2

from lentra.core.response.builder import build_response


class LentraPipeline:

    def __init__(self):
        self.market_v2 = MarketIntelligenceV2()
        self.risk_v2 = RiskEngineV2()
        self.ranker_v2 = RankerV2()
        self.area_v2 = ExpatAreaScoreV2()
        self.scorer_v2 = UnifiedScorerV2()
        self.ux_v2 = UXBuilderV2()

    def run(self, text: str):

        print("[PIPELINE] INPUT:", text)

        query = parse_query(text)
        print("[PIPELINE] QUERY:", query)

        listings = fetch_listings(query)
        listings = normalize(listings)
        listings = deduplicate(listings)

        market_v1 = estimate_market_price(listings, query)
        market_v2 = self.market_v2.build_market_context(listings, query)

        listings_v1 = score_risk(listings)

        enriched = []
        for item in listings_v1:

            try:
                v2_risk = self.risk_v2.score(item, market_v2)
                item["risk_score"] = v2_risk["risk_score"]
                item["risk_v2"] = v2_risk
            except Exception:
                item["risk_score"] = item.get("risk_score", 0)

            try:
                item["area_v2"] = self.area_v2.score(item)
            except Exception:
                item["area_v2"] = None

            try:
                item["ai_score_v2"] = self.scorer_v2.score(item, market_v2)
            except Exception:
                item["ai_score_v2"] = {"score": 0, "verdict": "unknown"}

            enriched.append(item)

        listings = self.ranker_v2.rank(enriched, market_v2)

        # UX LAYER BUILD
        ux_cards = [
            self.ux_v2.build_card(item, market_v2)
            for item in listings
        ]

        response = build_response(ux_cards, market_v2, query)

        print("[PIPELINE] DONE")

        return response
