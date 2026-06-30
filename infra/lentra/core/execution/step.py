from typing import Protocol
from lentra.core.execution.execution_context import ExecutionContext


class PipelineStep(Protocol):

    name: str

    def run(self, ctx: ExecutionContext) -> ExecutionContext:
        ...
