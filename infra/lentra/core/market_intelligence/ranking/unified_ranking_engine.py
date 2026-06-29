from lentra.core.market_intelligence.ranking.ranking_engine import MarketRankingEngine


class UnifiedRankingEngine:
    """
    SINGLE SOURCE OF TRUTH ranking engine (clean version).
    """

    def __init__(self):
        self.core = MarketRankingEngine()

    def rank(self, cards: list):
        return self.core.rank(cards)
