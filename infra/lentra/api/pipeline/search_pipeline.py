from typing import Dict, Any, List

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.adapters.search_adapter import SearchAdapter


class SearchPipeline:
    """
    Main Market Intelligence Search Pipeline.

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
    Decision Layer
    """

    def __init__(self):
        self.gateway = build_gateway_v3()
        self.adapter = SearchAdapter()

    def _build_decision(
        self,
        market: Dict[str, Any],
        area: Dict[str, Any],
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        price_score = market.get(
            "pricing_score",
            0.5
        )

        deviation = abs(
            market.get(
                "deviation",
                0
            )
        )

        area_score = area.get(
            "score",
            0.5
        )

        final_score = (
            price_score * 0.7
            +
            area_score * 0.3
        )

        if deviation <= 0.05:
            action = "BUY"
            reason = "Цена соответствует рынку."

        elif deviation <= 0.15:
            action = "REVIEW"
            reason = "Цена немного отличается от рынка, требуется проверка."

        elif market.get("direction") == "over":
            action = "NEGOTIATE"
            reason = "Цена выше рынка, возможен торг."

        else:
            action = "REVIEW"
            reason = "Предложение требует дополнительного анализа."

        return {
            "action": action,
            "score": round(
                final_score,
                4
            ),
            "confidence": round(
                0.7 + min(
                    area_score * 0.2,
                    0.2
                ),
                2
            ),
            "reason": reason
        }

    def run(
        self,
        payload: Dict[str, Any]
    ) -> Dict[str, Any]:

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

            decision = self._build_decision(
                market,
                area,
                listing
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

                    "market_analysis": {
                        "listing_price": listing.get(
                            "price"
                        ),
                        "market_price": context.get(
                            "market_price"
                        )
                    },

                    "intelligence": {
                        "area": area,
                        "market": market
                    },

                    "decision": decision
                }
            )

        return {
            "query": query,
            "count": len(results),
            "results": results
        }
