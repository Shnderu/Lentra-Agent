import os
import time
import traceback

from core.lifecycle.task_claim import TaskClaimer
from core.lifecycle.execution_envelope import ExecutionEnvelope

# CORE ENTRYPOINTS (intelligence layer, НЕ runtime)
from core.market_intelligence.verdict.verdict_engine import VerdictEngine
from core.market_intelligence.scoring_engine import ScoringEngine
from core.market_intelligence.engines.risk import RiskEngine


WORKER_ID = os.getenv("WORKER_ID", "worker-1")
DSN = os.getenv("DATABASE_DSN", "postgresql://postgres:postgres@localhost:5432/lentra")


class WorkerRuntime:
    """
    Clean runtime layer:
    - no business logic
    - no graph/execution engine duplication
    - only orchestration
    """

    def __init__(self):
        self.claimer = TaskClaimer(DSN)
        self.envelope = ExecutionEnvelope()

        # intelligence engines (core layer)
        self.verdict = VerdictEngine()
        self.scoring = ScoringEngine()
        self.risk = RiskEngine()

    def dispatch(self, task: dict, env: dict) -> dict:
        """
        Single entry execution router.
        Core is NOT modified.
        """

        task_type = task.get("type")

        if task_type == "risk":
            return self.risk.evaluate(env)

        if task_type == "score":
            return self.scoring.compute(env)

        if task_type == "verdict":
            return self.verdict.compute(env)

        raise ValueError(f"Unknown task type: {task_type}")

    def run_forever(self):
        print(f"[WORKER] started: {WORKER_ID}")

        while True:
            try:
                task = self.claimer.claim(WORKER_ID)

                if not task:
                    time.sleep(0.3)
                    continue

                env = self.envelope.build(task)

                try:
                    result = self.dispatch(task, env)
                    self.claimer.mark_done(task["id"], result)

                except Exception as e:
                    error = {
                        "error": str(e),
                        "trace": traceback.format_exc()
                    }
                    self.claimer.mark_failed(task["id"], str(error))

            except Exception as loop_error:
                print("[WORKER LOOP ERROR]", loop_error)
                time.sleep(1)


if __name__ == "__main__":
    WorkerRuntime().run_forever()
