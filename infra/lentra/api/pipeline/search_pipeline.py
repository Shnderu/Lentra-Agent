from typing import Dict, Any

from lentra.runtime.bootstrap.gateway_v3 import build_gateway_v3
from lentra.core.market_intelligence.candidates.repository import candidate_repository


class SearchPipeline:
    """
    Main search entrypoint.

    Flow:

    query
      ↓
    market context
      ↓
    candidates
      ↓
    intelligence engines
      ↓
    decision
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

        price = payload.get(
            "price",
            0
        )


        city = "da_nang"

        if "nha trang" in query.lower():
            city = "nha_trang"


        candidates = candidate_repository.search(
            city
        )


        results = []


        for listing in candidates:

            context = {
                "query": query,
                "price": listing["price"],
                "market_price": price or listing["price"]
            }


            area = self.gateway.run_engine(
                "area",
                context
            )

            market = self.gateway.run_engine(
                "market_intelligence",
                context
            )


            results.append(
                {
                    **listing,
                    "intelligence": {
                        "area": area,
                        "market": market
                    }
                }
            )


        return {
            "query": query,
            "city": city,
            "count": len(results),
            "results": results
        }
