from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3

from lentra.core.market_intelligence.fusion.fusion_engine_v2 import (
    build_fusion_engine_v2,
)

from lentra.core.market_intelligence.search.parsers.query_parser import (
    parse_query,
)

from lentra.core.market_intelligence.engines.pricing_engine import (
    PricingEngine,
)

from lentra.core.market_intelligence.engines.risk_engine import (
    RiskEngine,
)

from lentra.core.market_intelligence.engines.dedup_engine import (
    DedupEngine,
)

from lentra.core.market_intelligence.engines.area_engine import (
    AreaEngine,
)


class SearchPipeline:
    """
    Main Market Intelligence pipeline.

    Query
      ->
    Normalization
      ->
    Intelligence engines
      ->
    Fusion
      ->
    Decision
    """

    def __init__(self):

        self.gateway = build_gateway_v3()

        self.fusion = build_fusion_engine_v2()

        self.pricing = PricingEngine()
        self.risk = RiskEngine()
        self.dedup = DedupEngine()
        self.area = AreaEngine()


    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

        query = payload.get(
            "query",
            ""
        )

        parsed = parse_query(
            query
        )


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


        # BASE CONTRACT

        intelligence_context = dict(
            context
        )


        # ENGINE CHAIN

        intelligence_context = self.pricing.evaluate(
            intelligence_context
        )

        intelligence_context = self.risk.evaluate(
            intelligence_context
        )

        intelligence_context = self.dedup.evaluate(
            intelligence_context
        )

        intelligence_context = self.area.evaluate(
            intelligence_context
        )


        engine_results = {

            "pricing": intelligence_context.get(
                "pricing",
                {}
            ),

            "risk": intelligence_context.get(
                "risk",
                {}
            ),

            "dedup": intelligence_context.get(
                "dedup",
                {}
            ),

            "area": intelligence_context.get(
                "area",
                {}
            ),

            "signals": {
                "length": len(
                    parsed.get(
                        "tokens",
                        []
                    )
                )
            },
        }


        fusion = self.fusion.evaluate(
            engine_results
        )


        return {

            "query": query,

            "market_context": {

                "city": context["city"],

                "listing_price": context["price"],

                "market_price": context["market_price"],

            },


            "market_analysis": fusion.get(
                "market_analysis"
            ),


            "intelligence": fusion.get(
                "intelligence"
            ),


            "decision": {

                "decision": fusion.get(
                    "decision"
                ),

                "score": fusion.get(
                    "score"
                ),

            }
        }
