# ============================================================
# RENT SEARCH RANKING SERVICE LEGACY COMPATIBILITY V2
# ============================================================

"""
LEGACY APPLICATION FACADE

Ranking authority is owned by:

lentra.core.market_intelligence.ranking

This module exists only to preserve
old application imports.
"""


from lentra.application.rent_search.ranking_adapter import (
    RankingAdapter
)


class RentSearchRankingService:

    def __init__(self):

        self.ranker = RankingAdapter()


    def rank(
        self,
        items
    ):

        return self.ranker.rank(
            items
        )
