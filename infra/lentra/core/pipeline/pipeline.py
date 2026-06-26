from lentra.core.parsing.query_parser import parse_query
from lentra.core.data.fetcher import fetch_listings
from lentra.core.normalization.normalizer import normalize
from lentra.core.dedup.deduplicator import deduplicate

from lentra.core.market.pricing import estimate_market_price
from lentra.core.risk.risk_scorer import score_risk
from lentra.core.ranking.ranker import rank_listings

from lentra.core.v2.market.market_intelligence import MarketIntelligenceV2
from lentra.core.v2.risk.risk_engine import RiskEngineV2

from lentra.core.response.builder import build_response


class LentraPipeline:

    def __init__(self):
        self.market_v2 = MarketIntelligenceV2()
        self.risk_v2 = RiskEngineV2()

    def run(self, text: str):

        print("[PIPELINE] INPUT:", text)

        query = parse_query(text)
        print("[PIPELINE] QUERY:", query)

        listings = fetch_listings(query)
        listings = normalize(listings)
        listings = deduplicate(listings)

        # -------------------------
        # V1 MARKET
        # -------------------------
        market_v1 = estimate_market_price(listings, query)

        # -------------------------
        # V2 MARKET (SHADOW)
        # -------------------------
        market_v2 = self.market_v2.build_market_context(listings, query)

        print("[PIPELINE] MARKET V1:", market_v1)
        print("[PIPELINE] MARKET V2:", market_v2)

        # -------------------------
        # V1 RISK (CURRENT)
        # -------------------------
        listings_v1 = score_risk(listings, market_v1)

        # -------------------------
        # V2 RISK (SHADOW)
        # -------------------------
        listings_v2 = []
        for item in listings:
            try:
                listings_v2.append(self.risk_v2.score(item, market_v2))
            except Exception as e:
                print("[V2 RISK ERROR]", e)

        # -------------------------
        # V1 RANKING (STABLE)
        # -------------------------
        listings = rank_listings(listings_v1)

        response = build_response(listings, market_v1, query)

        print("[PIPELINE] DONE")

        return response
