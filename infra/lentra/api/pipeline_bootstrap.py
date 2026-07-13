"""
Legacy API pipeline bootstrap.

Retired:
    direct GatewayV3 initialization

Canonical API execution path:

    API
      ->
    SearchPipeline
      ->
    GatewayV3
      ->
    Market Intelligence Core

This module remains as compatibility placeholder.
"""


from typing import Any, Dict


class Orchestrator:
    """
    Compatibility wrapper.

    Deprecated:
        legacy gateway orchestration
    """

    def __init__(self, gateway: Dict[str, Any] | None = None):
        self.gateway = gateway

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        if self.gateway is None:
            return {
                "status": "retired",
                "message": "Use canonical SearchPipeline execution path"
            }

        return self.gateway["handle"](request)


def build_orchestrator():
    return Orchestrator(
        gateway=None
    )
