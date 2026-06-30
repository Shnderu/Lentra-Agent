try:
    from lentra.core.runtime.trace.runtime_trace_layer import RuntimeTraceLayer
    _TRACE = RuntimeTraceLayer()
except Exception:
    _TRACE = None

"""
BOOTSTRAP ENTRYPOINT (CLEAN)

RULE:
- NO business logic imports
- ONLY wiring layer
- NO orchestrator dependency
"""

from lentra.core.market_intelligence.build import build_intelligence_gateway


def get_gateway(orchestrator=None):
    """
    Pure entrypoint factory.
    Does NOT import orchestrator or pipeline.
    """
    return build_intelligence_gateway(orchestrator=orchestrator)
