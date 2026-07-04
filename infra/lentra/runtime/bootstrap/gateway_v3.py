from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GatewayV3:
    engines: Dict[str, Any]
    engine_isolator: Any = None


def build_gateway_v3() -> GatewayV3:
    gateway = GatewayV3(engines={})

    # ❌ REMOVE importlib.reload (source of instability)
    from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine

    # 🔒 deterministic init (no runtime mutation)
    engine = MarketIntelligenceEngine()

    gateway.engines["market_intelligence"] = engine

    from lentra.runtime.bootstrap.engine_isolator import EngineIsolator
    gateway.engine_isolator = EngineIsolator(gateway.engines)

    return gateway
