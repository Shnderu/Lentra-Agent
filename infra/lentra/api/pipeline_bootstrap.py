from typing import Any, Dict

from lentra.runtime.bootstrap.wiring_safe import build_gateway


class Orchestrator:
    """
    API orchestration layer.

    Core intelligence:
    RegistryV3 + FusionEngineV2
    """

    def __init__(self, gateway: Dict[str, Any]):
        self.gateway = gateway

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        return self.gateway["handle"](request)


def build_orchestrator():

    gateway = build_gateway()

    return Orchestrator(
        gateway=gateway
    )
