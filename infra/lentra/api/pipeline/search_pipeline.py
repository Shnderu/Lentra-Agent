from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.market_intelligence.data.city_profiles import get_market_price
from lentra.core.market_intelligence.search.parsers.query_parser import parse_query


class SearchPipeline:
    """
    Single entrypoint for /search API

    Flow:
    query
      ->
    parser
      ->
    city profile
      ->
    market intelligence
      ->
    decision
    """

    def __init__(self):
        self.gateway = build_gateway_v3()

    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        query_text = payload.get(
            "query",
            ""
        )

        parsed = parse_query(
            query_text
        )

        city = parsed.get(
            "city",
            "da_nang"
        )

        market_price = parsed.get(
            "market_price"
        )

        price = payload.get(
            "price"
        )

        if price is None:
            price = parsed.get(
                "budget",
                0
            )

        context = {
            "query": query_text,
            "city": city,
            "price": price,
            "market_price": market_price,
        }

        area = self.gateway.run_engine(
            "area",
            context
        )

        market = self.gateway.run_engine(
            "market_intelligence",
            context
        )

        score = 0.5

        if isinstance(
            market,
            dict
        ):
            score = market.get(
                "pricing_score",
                0.5
            )

        decision = (
            "BUY"
            if score >= 0.7
            else "REVIEW"
            if score >= 0.45
            else "AVOID"
        )

        return {
            "query": query_text,

            "market_context": {
                "city": city,
                "listing_price": price,
                "market_price": market_price,
            },

            "features": {
                "area": area,
                "market_intelligence": market,
            },

            "decision": {
                "decision": decision,
                "final_score": score,
                "confidence": 0.8
            }
        }
