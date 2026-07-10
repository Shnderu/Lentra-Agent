from lentra.core.market_intelligence.engines import build_engines
from lentra.core.market_intelligence.registry.engine_registry import build_registry
from lentra.core.market_intelligence.fusion.fusion_engine_v2 import build_fusion_engine_v2


def build_gateway():

    engines = build_engines()

    registry = build_registry(engines)

    fusion = build_fusion_engine_v2()

    gateway = {
        "registry": registry,
        "fusion": fusion,
        "handle": lambda payload: fusion.evaluate(
            registry.evaluate(payload)
        )
    }

    return gateway
