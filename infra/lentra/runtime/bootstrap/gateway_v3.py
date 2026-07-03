from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GatewayV3:
    engines: Dict[str, Any]
    engine_isolator: Any = None


def build_gateway_v3() -> GatewayV3:
    """
    Canonical gateway builder.
    Ensures strict object model (no dict-based gateway).
    """

    gateway = GatewayV3(engines={})

    engines = getattr(gateway, "engines", None)
    if engines is None:
        engines = {}

    gateway.engines = engines

    # isolation layer (safe attach)
    from lentra.runtime.bootstrap.engine_isolator_v3 import EngineIsolatorV3

    gateway.engine_isolator = EngineIsolatorV3(engines)

    return gateway
