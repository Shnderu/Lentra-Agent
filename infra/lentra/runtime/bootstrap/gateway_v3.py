from lentra.core.market_intelligence.engines.market_intelligence_engine import MarketIntelligenceEngine
from lentra.core.area.area_engine import AreaEngine
from lentra.runtime.bootstrap.engine_isolator import EngineIsolator


def build_gateway_v3():

    gateway = type("Gateway", (), {})()

    gateway.engines = {}

    # CORE ENGINE
    gateway.engines["market_intelligence"] = MarketIntelligenceEngine({})

    # AREA ENGINE (Vietnam geo layer)
    gateway.engines["area"] = AreaEngine({})

    # ISOLATOR
    gateway.engine_isolator = EngineIsolator(gateway.engines)

    return gateway
