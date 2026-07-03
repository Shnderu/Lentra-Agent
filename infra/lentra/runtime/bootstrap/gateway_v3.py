from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GatewayV3:
    engines: Dict[str, Any]
    engine_isolator: Any = None


def build_gateway_v3() -> GatewayV3:
    gateway = GatewayV3(engines={})

    # IMPORT ENGINE
    from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine

    # REGISTER ENGINE
    gateway.engines["market_intelligence"] = MarketIntelligenceEngine({})

    # ISOLATOR
    from lentra.runtime.bootstrap.engine_isolator import EngineIsolator
    gateway.engine_isolator = EngineIsolator(gateway.engines)

    return gateway
