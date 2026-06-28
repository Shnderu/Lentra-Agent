
from lentra.core.contracts.pipeline_context import PipelineContext
from lentra.core.modules.market.market_module import MarketModule
from lentra.core.modules.risk.risk_module import RiskModule
from lentra.core.modules.forecast.forecast_module import ForecastModule
from lentra.core.modules.decision.decision_module import DecisionModule
from lentra.core.modules.persona.persona_module import PersonaModule
from lentra.core.modules.ui.ui_module import UIModule

from lentra.core.market_intelligence.confidence.confidence_engine import ConfidenceEngine


class LentraPipeline:

    def run(self, raw):

        ctx = PipelineContext(raw)

        ctx = MarketModule().run(ctx)

        if not hasattr(ctx, "snapshot") or ctx.snapshot is None:
            raise RuntimeError("no snapshot")

        ctx.objects = ctx.snapshot.objects

        ctx = RiskModule().run(ctx)
        ctx = ForecastModule().run(ctx)

        # v2.1
        ctx.objects = ConfidenceEngine().run(ctx.objects)

        # v3 NEW
        ctx = DecisionModule().run(ctx)
        ctx = PersonaModule().run(ctx)
        ctx = UIModule().run(ctx)

        return ctx

