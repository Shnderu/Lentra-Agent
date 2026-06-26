from lentra.core.parsing.query_parser import parse_query
from lentra.core.data.fetcher import fetch_listings
from lentra.core.normalization.normalizer import normalize

from lentra.core.dedup.deduplicator import deduplicate as deduplicate_v1
from lentra.core.v2.dedup.deduplicator import deduplicate_v2

from lentra.core.market.pricing import estimate_market_price
from lentra.core.risk.risk_scorer import score_risk
from lentra.core.ranking.ranker import rank_listings
from lentra.core.response.builder import build_response


class LentraPipeline:

    def __init__(self, mode: str = "v1"):
        self.mode = mode

    def run(self, text: str):

        print("[PIPELINE] INPUT:", text)

        query = parse_query(text)
        print("[PIPELINE] QUERY:", query)

        listings = fetch_listings(query)
        listings = normalize(listings)

        # dedup switch
        if self.mode == "v2":
            listings = deduplicate_v2(listings)
        else:
            listings = deduplicate_v1(listings)

        market = estimate_market_price(listings, query)

        listings = score_risk(listings, market)
        listings = rank_listings(listings)

        response = build_response(listings, market, query)

        print("[PIPELINE] DONE")
        return response
