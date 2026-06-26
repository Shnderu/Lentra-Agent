from lentra.core.parsing.query_parser import parse_query
from lentra.core.data.fetcher import fetch_listings
from lentra.core.normalization.normalizer import normalize
from lentra.core.dedup.deduplicator import deduplicate
from lentra.core.market.pricing import estimate_market_price
from lentra.core.risk.risk_scorer import score_risk
from lentra.core.ranking.ranker import rank_listings
from lentra.core.response.builder import build_response


class LentraPipeline:

    def run(self, text: str):

        print("[PIPELINE] INPUT:", text)

        query = parse_query(text)
        print("[PIPELINE] QUERY:", query)

        listings = fetch_listings(query)
        print("[PIPELINE] FETCH:", type(listings), listings[:1] if listings else None)

        listings = normalize(listings)
        print("[PIPELINE] NORMALIZE:", type(listings), listings[:1] if listings else None)

        listings = deduplicate(listings)
        print("[PIPELINE] DEDUP:", type(listings), listings[:1] if listings else None)

        clean_listings = []
        for item in listings:
            print("[PIPELINE] ITEM TYPE:", type(item), item)

            if isinstance(item, dict):
                clean_listings.append(item)
            else:
                clean_listings.append({
                    "raw": str(item),
                    "price": None,
                    "description": ""
                })

        market = estimate_market_price(query, listings)

        enriched = []
        for item in clean_listings:
            risk = score_risk(item)
            item["risk"] = risk
            enriched.append(item)

        listings = rank_listings(enriched)

        response = build_response(listings, market, query)

        print("[PIPELINE] DONE")

        return response
