from typing import Dict, Any

from lentra.core.engines.engine_wrapper import EngineWrapper
from lentra.core.engines.area_engine import AreaEngine
from lentra.core.engines.market_intelligence_engine import MarketIntelligenceEngine


class GatewayV3:
    """
    Clean Gateway abstraction for Lentra AI OS.
    Responsibility:
      - engine orchestration only
      - NO business logic
    """

    def __init__(self):
        self.engines: Dict[str, Any] = {}

    def register(self, name: str, engine: Any):
        self.engines[name] = EngineWrapper(engine)
        return self

    def run_engine(self, name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.engines:
            return {
                "error": f"engine_not_found:{name}",
                "fallback": True
            }

        return self.engines[name](context)


def build_gateway_v3() -> GatewayV3:
    gateway = GatewayV3()

    # IMPORTANT:
    # FIX: NO engine(config) construction
    # engines are pure classes now

    gateway.register("area", AreaEngine)
    gateway.register("market_intelligence", MarketIntelligenceEngine)

    return gateway
