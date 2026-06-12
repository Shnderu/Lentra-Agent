import json
import subprocess
from core.reasoning.reasoning_engine import ReasoningEngine

class ClosedLoopOptimizer:

    def __init__(self):
        self.reasoning = ReasoningEngine()

        # SAFE CONFIG SPACE (allowlist only)
        self.config = {
            "worker_concurrency": 1,
            "retry_backoff": 1,
            "stream_batch_size": 1
        }

    # -----------------------------
    # METRICS SNAPSHOT
    # -----------------------------
    def snapshot(self):
        def cmd(c):
            return subprocess.getoutput(c)

        return {
            "tasks": int(cmd("docker exec -i lentra-redis redis-cli XLEN stream:rent:tasks")),
            "results": int(cmd("docker exec -i lentra-redis redis-cli XLEN stream:rent:results")),
            "pending": cmd("docker exec -i lentra-redis redis-cli XPENDING stream:rent:tasks workers")
        }

    # -----------------------------
    # SAFE OPTIMIZATION POLICY
    # -----------------------------
    def propose(self, metrics, diagnosis):
        rc = diagnosis["root_cause"]

        proposals = []

        if rc == "PIPELINE_EXECUTION_STUCK":
            proposals.append({
                "config": "worker_concurrency",
                "from": self.config["worker_concurrency"],
                "to": 2,
                "reason": "Increase throughput to unblock pipeline"
            })

        if rc == "SERIALIZATION_FAILURE":
            proposals.append({
                "config": "stream_batch_size",
                "from": self.config["stream_batch_size"],
                "to": 1,
                "reason": "Force strict single-message serialization"
            })

        return proposals

    # -----------------------------
    # APPLY WITH SAFETY CHECK
    # -----------------------------
    def apply(self, proposals):
        for p in proposals:
            print(f"[OPTIMIZER] applying: {p}")

            # apply only allowed configs
            self.config[p["config"]] = p["to"]

    # -----------------------------
    # EVALUATE IMPACT (simple heuristic v1)
    # -----------------------------
    def evaluate(self, before, after):
        if after["results"] > before["results"]:
            return "IMPROVEMENT"
        if after["results"] == before["results"]:
            return "NO_CHANGE"
        return "DEGRADATION"

    # -----------------------------
    # ENTRYPOINT
    # -----------------------------
    def run(self):
        before = self.snapshot()

        reasoning = self.reasoning
        metrics = reasoning.rc.collect_metrics()
        diagnosis = reasoning.rc.analyze(metrics)

        proposals = self.propose(metrics, diagnosis)
        self.apply(proposals)

        after = self.snapshot()

        result = {
            "before": before,
            "after": after,
            "diagnosis": diagnosis,
            "proposals": proposals,
            "evaluation": self.evaluate(before, after)
        }

        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    ClosedLoopOptimizer().run()
