from typing import Any, Dict, Callable
import time


class EngineWrapperV1:
    """
    Unified execution layer for all engines

    FEATURES:
    - automatic timing
    - consistent interface
    - trace-ready output
    """

    def __init__(self, observability=None):
        self.obs = observability

    def run(self, engine_name: str, fn: Callable, ctx: Dict[str, Any]) -> Dict[str, Any]:

        start = time.time()

        # EXECUTION
        result = fn(ctx)

        duration = round((time.time() - start) * 1000, 6)

        # OBSERVABILITY HOOK
        if self.obs:
            self.obs.timings.append({
                "engine": engine_name,
                "duration_ms": duration
            })

        return result
