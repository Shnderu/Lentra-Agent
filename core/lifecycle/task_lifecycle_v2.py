import time

from core.lifecycle.task_lifecycle import TaskLifecycleEngine
from core.lifecycle.ai_native_orchestrator import AINativeOrchestrator


class TaskLifecycleEngineV2(TaskLifecycleEngine):
    """
    AI-native upgrade over base lifecycle engine.
    """

    def __init__(self):
        super().__init__()
        self.ai = AINativeOrchestrator()

    def process(self, task: dict):
        task_id = task.get("task_id")

        start = time.time()

        # 1. AI decides execution strategy
        strategy = self.ai.build_strategy(task)

        # attach strategy into telemetry
        self.tracer.span(task_id, "ai_strategy", strategy)

        # 2. override routing based on AI decision
        if strategy.get("providers"):
            task["forced_providers"] = strategy["providers"]

        # 3. execute base lifecycle
        result = super().process(task)

        # 4. feedback loop
        latency = time.time() - start
        score = self.ai.reward_signal(latency, result.get("status") == "done")

        self.tracer.span(task_id, "ai_feedback", {
            "latency": latency,
            "score": score
        })

        return result
