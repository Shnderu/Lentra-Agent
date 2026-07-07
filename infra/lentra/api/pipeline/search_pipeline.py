from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.market_intelligence.fusion.fusion_engine_v2 import (
    build_fusion_engine_v2,
)
from lentra.core.market_intelligence.search.parsers.query_parser import (
    parse_query,
)


class SearchPipeline:
    """
    Single entrypoint for /search API.

    Flow:
    query
      ->
    normalization
      ->
    market engines
      ->
    fusion intelligence
      ->
    decision
    """

    def __init__(self):
        self.gateway = build_gateway_v3()
        self.fusion = build_fusion_engine_v2()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        query = payload.get(
            "query",
            ""
        )

        parsed = parse_query(query)

        context = {
            "query": query,
            "price": payload.get(
                "price",
                parsed.get("budget", 0)
            ),
            "market_price": payload.get(
                "market_price",
                parsed.get("market_price", 0)
            ),
            "city": parsed.get(
                "city"
            ),
        }

        area = self.gateway.run_engine(
            "area",
            context
        )

        market = self.gateway.run_engine(
            "market_intelligence",
            context
        )

        engine_results = {
            "pricing": {
                "price": context["price"],
                "market_price": context["market_price"],
            },

            "risk": {
                "level": "low"
            },

            "signals": {
                "length": len(
                    parsed.get(
                        "tokens",
                        []
                    )
                )
            },

            "dedup": {
                "duplicates": 0
            },

            "area": area,

            "market_intelligence": market,
        }

        intelligence = self.fusion.evaluate(
            engine_results
        )

        return {
            "query": query,

            "market_context": {
                "city": context["city"],
                "listing_price": context["price"],
                "market_price": context["market_price"],
            },

            "intelligence": intelligence,

            "decision": {
                "decision": intelligence.get(
                    "decision"
                ),

                "score": intelligence.get(
                    "score"
                ),

                "confidence": market.get(
                    "confidence",
                    0.5
                ),
            }
        }
