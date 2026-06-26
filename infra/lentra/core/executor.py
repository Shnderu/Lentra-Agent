from dataclasses import dataclass
from typing import Any, Dict

from lentra.core.pipeline.pipeline import Pipeline
from lentra.core.context.runtime_context import RuntimeContext


@dataclass
class ExecutionResult:
    success: bool
    data: Any = None
    error: str = None


class Executor:
    """
    SINGLE EXECUTION ENTRYPOINT

    Архитектурное правило:
    - Executor НЕ принимает решений
    - Executor НЕ знает про scenario / graph / risk / pricing
    - Executor только делегирует в Pipeline
    """

    def __init__(self, pipeline: Pipeline):
        self.pipeline = pipeline

    def execute(self, task: Dict, context: RuntimeContext = None) -> ExecutionResult:
        """
        Единственная точка исполнения.

        Flow:
        task → pipeline → result
        """

        try:
            result = self.pipeline.execute(task=task, context=context)

            return ExecutionResult(
                success=True,
                data=result
            )

        except Exception as e:
            return ExecutionResult(
                success=False,
                error=str(e)
            )


# BACKWARD COMPATIBILITY ENTRY (если где-то импортится напрямую)
_default_executor = None


def get_executor(pipeline: Pipeline = None) -> Executor:
    global _default_executor

    if _default_executor is None:
        if pipeline is None:
            raise RuntimeError("Pipeline must be provided for first initialization")

        _default_executor = Executor(pipeline=pipeline)

    return _default_executor
