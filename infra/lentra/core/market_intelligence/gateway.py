from lentra.core.pipeline.context import PipelineContext
from lentra.core.market_intelligence.signals.signals_engine_v2 import SignalsEngineV2
from lentra.core.market_intelligence.risk.risk_engine import RiskEngine
from lentra.core.market_intelligence.ranking.ranking_engine import RankingEngine


class IntelligenceGateway:

    def __init__(self):
        self.signals = SignalsEngineV2()
        self.risk = RiskEngine()
        self.ranking = RankingEngine()

    def compute(self, payload: dict):

        ctx = PipelineContext(raw=payload)

        # STAGE 1
        ctx = self.signals.compute(ctx)

        # STAGE 2 (risk reads ONLY immutable ctx)
        ctx = self.risk.compute(ctx)

        # STAGE 3
        ctx = self.ranking.compute(ctx)

        return {
            "pricing": ctx.pricing,
            "area": ctx.area,
            "dedup": ctx.dedup,
            "coupling": ctx.coupling,
            "risk": ctx.risk,
            "ranking": ctx.ranking,
            "enrichment": ctx.enrichment,
        }
