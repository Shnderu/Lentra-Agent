# ============================================================
# SEARCH SERVICE V18 - MARKET INTELLIGENCE ENTRY
# ============================================================

import time

from lentra.core.adapters.search_adapter import SearchAdapter
from lentra.core.market_intelligence.market_intelligence_engine import (
    MarketIntelligenceEngine,
)


class SearchService:
    """
    Product search entrypoint.

    Flow:

    API
      |
      v
    SearchService
      |
      v
    SearchAdapter
      |
      v
    Market Intelligence Engine
      |
      v
    Decision Layer
    """

    def __init__(self):

        self.adapter = SearchAdapter()

        self.market_intelligence = MarketIntelligenceEngine()


    async def search(self, request: dict):

        start = time.time()

        query = request.get(
            "query",
            ""
        )

        objects = self.adapter.build_objects(
            query
        )

        if not objects:
            return {
                "items": [],
                "count": 0,
                "query": query,
                "mode": "market_intelligence_v18",
            }


        try:

            result = self.market_intelligence._run_core_graph(
                {
                    "query": query,
                    "objects": objects,
                }
            )

        except Exception as e:

            return {
                "status": "error",
                "error": str(e),
                "query": query,
                "mode": "market_intelligence_v18",
            }


        elapsed = round(
            time.time() - start,
            4
        )


        return {
            "items": result,
            "count": len(result)
            if isinstance(result, list)
            else 1,
            "query": query,
            "execution_time": elapsed,
            "mode": "market_intelligence_v18",
        }
