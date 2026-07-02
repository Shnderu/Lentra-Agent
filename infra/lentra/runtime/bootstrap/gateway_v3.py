from lentra.runtime.bootstrap.wiring_safe import build_gateway
from lentra.core.market_intelligence.isolation.engine_isolator import EngineIsolatorV3


def build_gateway_v3():
    gateway = build_gateway()

    engines = getattr(gateway, "engines", {})

    # FORCE ISOLATION LAYER
    gateway.engine_isolator = EngineIsolatorV3(engines)

    return gateway
