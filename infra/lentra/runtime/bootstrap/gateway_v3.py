from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GatewayV3:
    engines: Dict[str, Any]
    engine_isolator: Any = None


def build_gateway_v3() -> GatewayV3:
    gateway = GatewayV3(engines={})

    from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine
    gateway.engines["market_intelligence"] = MarketIntelligenceEngine({})

    # V2 isolator (primary)
    try:
        from lentra.runtime.bootstrap.engine_isolator_v2 import EngineIsolatorV2
        gateway.engine_isolator = EngineIsolatorV2(gateway.engines)
        gateway._isolator_version = "v2"
    except Exception:
        # fallback to v1 if anything breaks
        from lentra.runtime.bootstrap.engine_isolator import EngineIsolator
        gateway.engine_isolator = EngineIsolator(gateway.engines)
        gateway._isolator_version = "v1"

    return gateway
