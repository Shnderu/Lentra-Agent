from lentra.core.pipeline.context import PipelineContext
from lentra.core.modules.market.market_module import MarketModule
from lentra.core.modules.decision.decision_module import DecisionModule


class LentraPipeline:

    def __init__(self):
        self.market = MarketModule()
        self.decision = DecisionModule()

    def run(self, payload: dict):

        # 1. MARKET
        market_ctx = self.market.run(payload)

        # 2. ЖЁСТКАЯ НОРМАЛИЗАЦИЯ SNAPSHOT
        if isinstance(market_ctx, dict) and "objects" in market_ctx:
            from lentra.core.pipeline.context import Snapshot

            snapshot = Snapshot(objects=market_ctx["objects"])

            ctx = PipelineContext(
                query=market_ctx.get("query", ""),
                snapshot=snapshot,
                meta=market_ctx
            )
        else:
            # fallback safe state
            ctx = PipelineContext(
                query=str(payload),
                snapshot=Snapshot(objects=[]),
                meta={}
            )

        # 3. DECISION
        enriched = self.decision.run(ctx)

        return enriched
