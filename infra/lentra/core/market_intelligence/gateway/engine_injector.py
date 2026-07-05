from typing import Dict, Any

from lentra.core.market_intelligence.engines.engine_wrapper import EngineWrapper


class EngineInjector:
    """
    Safe injection layer for engines.

    Guarantees:
    - zero changes to engine logic
    - wrapper-only instrumentation
    """

    def __init__(self, tracer):
        self.tracer = tracer

    def inject(self, name: str, fn):
        return EngineWrapper(
            name=name,
            fn=fn,
            tracer=self.tracer
        )

    def call(self, wrapper: EngineWrapper, payload: Dict[str, Any], ctx: Dict[str, Any]) -> Dict[str, Any]:
        return wrapper.run(payload, ctx)
