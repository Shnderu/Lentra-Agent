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
    Main search pipeline.

    Flow:

    Query
      ->
    Parser
      ->
    Market engines
      ->
    Fusion Intelligence
      ->
    Decision
    """

    def __init__(self):
        self.gateway = build_gateway_v3()
        self.fusion = build_fusion_engine_v2()

    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = payload.get(
            "query",
            ""
        )

        parsed = parse_query(query)

        context = {
            "query": query,

            "price": payload.get(
                "price",
                parsed.get(
                    "budget",
                    0
                )
            ),

            "market_price": payload.get(
                "market_price",
                parsed.get(
                    "market_price",
                    0
                )
            ),

            "city": parsed.get(
                "city"
            ),
        }


        # MARKET INTELLIGENCE ENGINES

        area = self.gateway.run_engine(
            "area",
            context
        )

        market = self.gateway.run_engine(
            "market_intelligence",
            context
        )


        # NORMALIZED PRICING CONTRACT

        listing_price = context.get(
            "price",
            0
        )

        market_price = context.get(
            "market_price",
            0
        )


        if market_price:

            deviation = (
                listing_price - market_price
            ) / market_price

            delta = (
                listing_price - market_price
            )

            pricing_score = max(
                0.0,
                min(
                    1.0,
                    1 - abs(deviation)
                )
            )

        else:

            deviation = 0
            delta = 0
            pricing_score = 0.5


        pricing = {
            "price": listing_price,

            "market_price": market_price,

            "score": round(
                pricing_score,
                4
            ),

            "delta": round(
                delta,
                2
            ),

            "deviation": round(
                deviation,
                4
            )
        }


        engine_results = {

            "pricing": pricing,

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
        }


        intelligence = self.fusion.evaluate(
            engine_results
        )


        return {

            "query": query,

            "market_context": {
                "city": context["city"],

                "listing_price": listing_price,

                "market_price": market_price,
            },


            "market_analysis": intelligence.get(
                "market_analysis"
            ),


            "intelligence": intelligence.get(
                "intelligence"
            ),


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
