from typing import Dict, Any

from lentra.core.market_intelligence.engine_wrapper import EngineWrapper
from lentra.core.engines.area_engine import AreaEngine
from lentra.core.engines.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.observability.observability_engine_v1 import ObservabilityEngineV1


class GatewayV3:
    """
    Gateway orchestration layer.

    Responsibility:
    - engine routing only
    - no business logic
    """

    def __init__(self):
        self.engines: Dict[str, Any] = {}
        self.obs = ObservabilityEngineV1()

    def register(self, name: str, engine_cls):

        engine = engine_cls()

        self.engines[name] = EngineWrapper(
            name,
            engine.run,
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

    return gateway
