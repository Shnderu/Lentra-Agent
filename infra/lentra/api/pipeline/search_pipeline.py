from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.market_intelligence.search.parsers.query_parser import parse_query
from lentra.core.market_intelligence.data.city_profiles import get_market_price


class SearchPipeline:
    """
    Single entrypoint for /search API.

    MVP flow:
    query parsing
    ->
    market context enrichment
    ->
    intelligence engines
    """

    def __init__(self):
        self.gateway = build_gateway_v3()

    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = payload.get(
            "query",
            ""
        )

        parsed = parse_query(query)

        market_price = parsed.get(
            "market_price"
        )

        if not market_price:
            city = parsed.get(
                "city",
                "da_nang"
            )

            market_price = get_market_price(
                city
            )

        price = payload.get(
            "price"
        )

        if not price:
            price = parsed.get(
                "budget"
            )

        context = {
            "query": query,
            "city": parsed.get("city"),
            "price": price,
            "market_price": market_price,
            "parsed_query": parsed,
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

        if isinstance(market, dict):
            score = market.get(
                "pricing_score",
                0.5
            )

        decision = (
            "BUY"
            if score >= 0.6
            else "AVOID"
        )

        difference = (
            price - market_price
            if price is not None and market_price is not None
            else 0
        )

        difference_percent = (
            round(
                (difference / market_price) * 100,
                2
            )
            if market_price
            else 0
        )

        verdict = "market_price"

        if difference > 0:
            verdict = "overpriced"

        elif difference < 0:
            verdict = "good_deal"

        return {
            "query": query,

            "market_analysis": {
                "listing_price": price,
                "market_price": market_price,
                "difference": difference,
                "difference_percent": difference_percent,
                "verdict": verdict,
            },

            "features": {
                "area": area,
                "market_intelligence": market,
            },

            "decision": {
                "decision": decision,
                "final_score": score,
                "confidence": 0.8,
            }
        }
