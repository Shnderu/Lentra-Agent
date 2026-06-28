from lentra.core.modules.market.market_module import MarketModule
from lentra.core.modules.risk.risk_module import RiskModule
from lentra.core.modules.forecast.forecast_module import ForecastModule
from lentra.core.modules.decision.decision_module import DecisionModule
from lentra.core.modules.persona.persona_module import PersonaModule
from lentra.core.modules.ui.ui_module import UIModule

from lentra.core.market_intelligence.persona.persona_engine import PersonaEngine
from lentra.core.market_intelligence.normalizer.safety_normalizer import SafetyNormalizer

from lentra.core.contracts.pipeline_context import PipelineContext


class LentraPipeline:

    def run(self, raw):

        ctx = PipelineContext(raw)

        ctx = MarketModule().run(ctx)

        ctx = RiskModule().run(ctx)
        ctx = ForecastModule().run(ctx)

        ctx = PersonaModule().run(ctx)
        ctx = PersonaEngine().run(ctx)

        ctx = DecisionModule().run(ctx)

        ctx = SafetyNormalizer().run(ctx)

        ctx = UIModule().run(ctx)

        # 🔥 FIX: RESTORE CONTRACT
        ctx.snapshot = ctx.snapshot if hasattr(ctx, "snapshot") else ctx.market_snapshot

        return ctx
