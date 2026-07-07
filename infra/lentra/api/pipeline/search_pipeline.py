from typing import Dict, Any, List

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.adapters.search_adapter import SearchAdapter


class SearchPipeline:
    """
    Main search pipeline.

    Flow:

    query
      |
      v
    SearchAdapter
      |
      v
    Market Intelligence Gateway
      |
      v
    AI Decision
    """

    def __init__(self):
        self.gateway = build_gateway_v3()
        self.adapter = SearchAdapter()

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        query = payload.get(
            "query",
            ""
        )

        listings = self.adapter.build_objects(
            query
        )

        results: List[Dict[str, Any]] = []

        for listing in listings:

            context = {
                "query": query,
                "price": listing.get(
                    "price",
                    0
                ),
                "market_price": listing.get(
                    "market_price",
                    650
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
            )

            results.append(
                {
                    "id": listing.get(
                        "id"
                    ),

                    "title": listing.get(
                        "title"
                    ),

                    "price": listing.get(
                        "price"
                    ),

                    "city": listing.get(
                        "city",
                        "da_nang"
                    ),

                    "source": listing.get(
                        "source",
                        "seed"
                    ),

                    "intelligence": {
                        "area": area,
                        "market": market
                    },

                    "decision": {
                        "decision": decision,
                        "score": round(
                            score,
                            4
                        )
                    }
                }
            )

        return {
            "query": query,

            "count": len(
                results
            ),

            "results": results
        }
