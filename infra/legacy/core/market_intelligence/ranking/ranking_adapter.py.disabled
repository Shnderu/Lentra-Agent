from lentra.core.market_intelligence.ranking.unified_ranking_engine import (
    UnifiedRankingEngine
)


class RankingAdapter:
    """
    Compatibility adapter.

    Bot search pipeline delegates ranking
    to Market Intelligence ranking authority.
    """

    def __init__(self):
        self.engine = UnifiedRankingEngine()

    def rank(self, items):

        if not isinstance(items, list):
            return []

        return self.engine.rank(items)
