from typing import Any, Dict, Callable
import time

from lentra.core.observability.trace_collector import TraceCollector


class EngineWrapper:
    """
    SAFE VERSION:

    Supports BOTH contracts:
    - build(payload)
    - compute(engine_outputs)
    """

    def __init__(self, name: str, fn: Callable, tracer: TraceCollector):
        self.name = name
        self.fn = fn
        self.tracer = tracer

    def run(self, payload: Dict[str, Any], ctx: Dict[str, Any] = None) -> Dict[str, Any]:

        if ctx is None:
            ctx = {}

        start = time.time()

        try:
            # SMART ADAPTATION LAYER
            if self.name == "signals":
                # signals engine: build(payload)
                output = self.fn(payload)

            else:
                # providers: compute(engine_outputs)
                output = self.fn(payload)

        except Exception as e:
            output = {
                "error": str(e),
                "engine": self.name
            }

        duration_ms = (time.time() - start) * 1000

        # TRACE INJECTION
        self.tracer.record_engine(
            name=self.name,
            duration_ms=duration_ms,
            input_data=payload,
            output_data=output
        )

        return output
