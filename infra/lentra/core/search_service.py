# ============================================================
# LENTRA MVP SEARCH SERVICE
# ============================================================

from lentra.core.ranker import Ranker
from lentra.core.normalizer import Normalizer
from lentra.data.connectors.mock import MockConnector


class SearchService:

    def __init__(self):
        self.connector = MockConnector()
        self.normalizer = Normalizer()
        self.ranker = Ranker()

    async def search(self, request: dict):
        query = request.get("query", "")

        # 1. FETCH DATA
        raw_listings = self.connector.fetch(query)

        # 2. NORMALIZE
        listings = self.normalizer.transform(raw_listings)

        # 3. RANK
        ranked = self.ranker.rank(listings, request)

        # 4. RESPONSE
        return self._build_response(ranked)

    def _build_response(self, ranked):
        if not ranked:
            return {"results": [], "message": "no data"}

        best = ranked[0]
        return {
            "best_choice": best,
            "alternatives": ranked[1:3],
            "confidence": best.get("score", 0.5)
        }
