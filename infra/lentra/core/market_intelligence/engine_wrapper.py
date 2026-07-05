from typing import Callable, Dict, Any
from lentra.core.observability.observability_engine_v1 import ObservabilityEngineV1


class EngineWrapper:
    """
    Safe execution wrapper:
    - normalizes signature
    - injects observability
    - prevents argument mismatch crashes
    """

    def __init__(self, engine_name: str, fn: Callable, obs: ObservabilityEngineV1):
        self.engine_name = engine_name
        self.fn = fn
        self.obs = obs

    def __call__(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        def safe_exec():
            # 🔒 FIX: always pass single ctx
            return self.fn(ctx)

        return self.obs.trace(
            self.engine_name,
            safe_exec
        )
