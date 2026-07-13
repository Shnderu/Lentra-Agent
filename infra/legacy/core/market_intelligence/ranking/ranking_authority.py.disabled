from lentra.core.market_intelligence.ranking.unified_ranking_engine import (
    UnifiedRankingEngine
)


class RankingAuthority:
    """
    Single ranking entry point.

    Decision layer and other consumers
    must not depend on concrete ranking engines.
    """

    def __init__(self):

        self.engine = UnifiedRankingEngine()


    def rank(
        self,
        listings: list,
        market_truth: dict | None = None
    ):

        if not isinstance(listings, list):
            return []

        return self.engine.rank(
            listings,
            market_truth
        )
