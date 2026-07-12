# ============================================================
# RENT SEARCH PIPELINE V3 - MARKET INTELLIGENCE RANKING
# ============================================================

from lentra.core.market_intelligence.ranking.ranking_adapter import (
    RankingAdapter
)


class SearchPipeline:
    """
    Search pipeline.

    Ranking responsibility delegated to
    Market Intelligence OS.
    """

    def __init__(self):
        self.ranker = RankingAdapter()

    def run(self, query: str, candidates: list):

        if not candidates:
            return []

        ranked = self.ranker.rank(candidates)

        return {
            "query": query,
            "results": ranked,
            "count": len(ranked),
            "mode": "market_intelligence_ranking_v1"
        }
