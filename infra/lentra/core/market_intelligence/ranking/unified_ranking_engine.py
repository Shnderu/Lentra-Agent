from lentra.core.market_intelligence.ranking.ranking_engine import MarketRankingEngine


class UnifiedRankingEngine:
    """
    SINGLE SOURCE OF TRUTH ranking engine.
    """

    def __init__(self):

        self.core = MarketRankingEngine()


    def rank(
        self,
        cards: list,
        market_truth=None
    ):

        return self.core.rank(
            cards,
            market_snapshot=market_truth
        )
