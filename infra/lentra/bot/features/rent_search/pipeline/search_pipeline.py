# ============================================================
# RENT SEARCH PIPELINE V4 - APPLICATION BOUNDARY
# ============================================================

from lentra.application.rent_search.ranking import (
    RentSearchRankingService
)


class SearchPipeline:
    """
    Search pipeline.

    Delivery layer delegates ranking
    through application boundary.
    """

    def __init__(self):

        self.ranker = RentSearchRankingService()


    def run(
        self,
        query: str,
        candidates: list
    ):

        if not candidates:
            return []


        ranked = self.ranker.rank(
            candidates
        )


        return {
            "query": query,
            "results": ranked,
            "count": len(ranked),
            "mode": "market_intelligence_ranking_v1"
        }
