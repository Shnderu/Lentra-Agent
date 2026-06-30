from lentra.core.market_intelligence._import_safety import ImportGuard


class MarketIntelligenceEngine:

    def __init__(self, config=None):
        with ImportGuard("MarketIntelligenceEngine"):
            self.config = config or {}

            # lazy attach only
            self._ranking = None
            self._dedup = None
            self._risk = None

    def ranking(self):
        if self._ranking is None:
            from lentra.core.market_intelligence.ranking.unified_ranking_engine import UnifiedRankingEngine
            self._ranking = UnifiedRankingEngine()
        return self._ranking

    def dedup(self):
        if self._dedup is None:
            from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
            self._dedup = UnifiedDedupEngine()
        return self._dedup

    def risk(self):
        if self._risk is None:
            from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2
            self._risk = RiskEngineV2()
        return self._risk
