from typing import Dict, Any

from lentra.core.market_intelligence.engine_wrapper import EngineWrapper
from lentra.core.engines.area_engine import AreaEngine
from lentra.core.engines.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine
from lentra.core.observability.observability_engine_v1 import ObservabilityEngineV1


class GatewayV3:
    """
    Gateway V3 orchestration layer.

    Responsibility:
    - routing only
    - no business logic
    """

    def __init__(self):
        self.engines: Dict[str, Any] = {}
        self.obs = ObservabilityEngineV1()

    def register(self, name: str, engine_cls):

        engine = engine_cls()

        if hasattr(engine, "run"):
            fn = engine.run

        elif hasattr(engine, "evaluate"):
            fn = engine.evaluate

        else:
            raise RuntimeError(
                f"engine_has_no_entrypoint:{name}"
            )

        self.engines[name] = EngineWrapper(
            name,
            fn,
            self.obs
        )

        return self

    def run_engine(
        self,
        name: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:

        if name not in self.engines:
            return {
                "error": f"engine_not_found:{name}",
                "fallback": True
            }

        return self.engines[name](context)


def build_gateway_v3():

    gateway = GatewayV3()

    gateway.register(
        "area",
        AreaEngine
    )

    gateway.register(
        "market_intelligence",
        MarketIntelligenceEngine
    )

    gateway.register(
        "risk",
        RiskEngine
    )

    gateway.register(
        "dedup",
        DedupEngine
    )

    return gateway
