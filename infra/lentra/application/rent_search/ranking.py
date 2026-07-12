from lentra.core.market_intelligence.ranking.ranking_adapter import (
    RankingAdapter
)


class RentSearchRankingService:
    """
    Application boundary for rent search ranking.

    Delivery layer must not access
    Market Intelligence directly.
    """

    def __init__(self):
        self.ranker = RankingAdapter()

    def rank(self, items):

        return self.ranker.rank(items)
