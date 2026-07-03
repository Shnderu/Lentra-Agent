from lentra.core.market_intelligence.engines import build_engines
from lentra.core.market_intelligence.isolation.engine_registry_v3 import build_registry_v3
from lentra.core.market_intelligence.fusion.fusion_engine_v2 import build_fusion_engine_v2


def build_gateway():
    engines = build_engines()

    registry = build_registry_v3(engines)

    fusion = build_fusion_engine_v2()

    gateway = {
        "registry": registry,
        "fusion": fusion,
        "handle": lambda payload: fusion.evaluate(registry.evaluate(payload))
    }

    return gateway
