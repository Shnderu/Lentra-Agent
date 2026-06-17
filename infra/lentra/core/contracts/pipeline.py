from dataclasses import dataclass
from typing import Any, List
from lentra.core.contracts.pipeline_lock import PipelineLock


@dataclass
class PipelineStep:
    name: str
    handler: Any


@dataclass
class Pipeline:
    steps: List[PipelineStep]

    def __post_init__(self):
        PipelineLock.assert_locked()

    def execute(self, context, input_data):
        data = input_data

        for step in self.steps:
            context.pipeline_state[step.name] = "running"
            data = step.handler(data, context)
            context.pipeline_state[step.name] = "done"

        return data
