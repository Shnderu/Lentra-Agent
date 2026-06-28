from lentra.core.context.ai_context import AIContext, Snapshot
from lentra.core.modules.decision.decision_module import DecisionModule
from lentra.core.data_layer.builders.task_builder import build_task
from lentra.core.data_layer.data_layer import DataLayer


class LentraPipeline:
    def __init__(self):
        self.decision = DecisionModule()
        self.data_layer = DataLayer()

    def run(self, payload: dict):
        task = build_task(payload)

        objects = self.data_layer.fetch(task["query"]) if hasattr(self.data_layer, "fetch") else []

        ctx = AIContext(
            title=task["query"],
            snapshot=Snapshot(objects=objects)
        )

        return self.decision.run(ctx)
