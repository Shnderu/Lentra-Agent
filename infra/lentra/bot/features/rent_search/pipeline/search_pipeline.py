# ============================================================
# RENT SEARCH PIPELINE V2 - CLEAN SAFE VERSION
# ============================================================

from lentra.bot.features.rent_search.ranking.ranking_service import RankingService


class SearchPipeline:
    """
    Clean pipeline without any shell injection artifacts.
    """

    def __init__(self):
        self.ranker = RankingService()

    def run(self, query: str, candidates: list):
        """
        Executes search pipeline:
        1. receives candidates
        2. ranks them
        3. returns sorted results
        """

        if not candidates:
            return []

        ranked = self.ranker.rank(candidates)

        return {
            "query": query,
            "results": ranked,
            "count": len(ranked),
            "mode": "safe_pipeline_v2"
        }
