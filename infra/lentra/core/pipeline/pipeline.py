from lentra.core.parsing.query_parser import parse_query
from lentra.core.geo.v2.router.geo_router import GeoRouterV2

from lentra.core.data.fetcher import fetch_listings
from lentra.core.normalization.normalizer import normalize
from lentra.core.dedup.deduplicator import deduplicate
from lentra.core.market.pricing import estimate_market_price
from lentra.core.risk.risk_scorer import score_risk
from lentra.core.ranking.ranker import rank_listings
from lentra.core.response.builder import build_response


class LentraPipeline:

    def __init__(self):
        self.geo = GeoRouterV2()

    def run(self, text: str):

        print("[PIPELINE] INPUT:", text)

        query = parse_query(text)
        print("[PIPELINE] QUERY:", query)

        # GEO ROUTING V2 (NEW)
        query = self.geo.route(query)
        print("[PIPELINE] GEO:", query)

        listings = fetch_listings(query)
        listings = normalize(listings)
        listings = deduplicate(listings)

        market = estimate_market_price(listings, query)

        listings = score_risk(listings, market)
        listings = rank_listings(listings)

        response = build_response(listings, market, query)

        print("[PIPELINE] DONE")

        return response
