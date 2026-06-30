
from typing import List
from lentra.core.execution.execution_context import ExecutionContext
from lentra.core.execution.step import PipelineStep


class ExecutionGraph:

    def __init__(self, steps: List[PipelineStep]):
        self.steps = steps

    def run(self, ctx: ExecutionContext):

        for step in self.steps:
            ctx = step.run(ctx)

        return ctx
