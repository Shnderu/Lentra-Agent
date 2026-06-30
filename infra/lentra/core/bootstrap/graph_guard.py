"""
EXECUTION ENFORCEMENT LAYER
Strict runtime validation for Intelligence Graph OS
"""

from typing import Any, Dict, List


class GraphExecutionGuard:
    """
    Ensures strict execution of intelligence graph steps.
    Prevents silent fallback execution.
    """

    def __init__(self):
        self.required_engines = [
            "pricing",
            "dedup",
            "risk",
            "ranking",
            "geo",
            "explanation"
        ]

    def validate_pipeline(self, pipeline: Any) -> None:
        """
        Validate that pipeline has required execution steps.
        Fail fast if graph is incomplete.
        """
        if not hasattr(pipeline, "steps") or not pipeline.steps:
            raise RuntimeError("[GRAPH_GUARD] Pipeline steps missing")

    def validate_engines(self, registry: Dict[str, Any]) -> None:
        """
        Ensure all critical engines are bound.
        """
        missing = []

        for engine in self.required_engines:
            if engine not in registry or registry[engine] is None:
                missing.append(engine)

        if missing:
            raise RuntimeError(
                f"[GRAPH_GUARD] Missing engine bindings: {missing}"
            )

    def enforce_step_execution(self, step: Any) -> None:
        """
        Ensure step is valid before execution.
        """
        if step is None:
            raise RuntimeError("[GRAPH_GUARD] Null step detected")

        if not hasattr(step, "execute"):
            raise RuntimeError("[GRAPH_GUARD] Invalid step contract")
