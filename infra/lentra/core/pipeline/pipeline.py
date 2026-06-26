from lentra.core.parsing.query_parser import parse_query
from lentra.core.data.fetcher import fetch_listings
from lentra.core.normalization.normalizer import normalize
from lentra.core.dedup.deduplicator import deduplicate

from lentra.core.market.pricing import estimate_market_price
from lentra.core.risk.risk_scorer import score_risk

from lentra.core.v2.market.market_intelligence import MarketIntelligenceV2
from lentra.core.v2.risk.risk_engine import RiskEngineV2

from lentra.core.v2.ranking.ranker_v2 import RankerV2

from lentra.core.response.builder import build_response


class LentraPipeline:

    def __init__(self):
        self.market_v2 = MarketIntelligenceV2()
        self.risk_v2 = RiskEngineV2()
        self.ranker_v2 = RankerV2()

    def run(self, text: str):

        print("[PIPELINE] INPUT:", text)

        query = parse_query(text)
        print("[PIPELINE] QUERY:", query)

        listings = fetch_listings(query)
        listings = normalize(listings)
        listings = deduplicate(listings)

        market_v1 = estimate_market_price(listings, query)
        market_v2 = self.market_v2.build_market_context(listings, query)

        print("[PIPELINE] MARKET V2 ACTIVE")

        # v1 risk
        listings = score_risk(listings)

        # attach v2 risk signals
        enriched = []
        for item in listings:
            try:
                v2 = self.risk_v2.score(item, market_v2)
                item["risk_v2"] = v2
                item["risk_score"] = v2["risk_score"]
            except Exception as e:
                print("[V2 RISK ERROR]", e)
                item["risk_score"] = item.get("risk_score", 0)

            enriched.append(item)

        listings = enriched

        # v2 ranking
        listings = self.ranker_v2.rank(listings, market_v2)

        response = build_response(listings, market_v2, query)

        print("[PIPELINE] DONE")

        return response
