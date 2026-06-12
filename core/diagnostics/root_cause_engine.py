import subprocess
import json

class RootCauseEngine:

    def __init__(self, redis_cli="docker exec -i lentra-redis redis-cli"):
        self.redis = redis_cli

    # -----------------------------
    # DATA COLLECTION
    # -----------------------------
    def collect_metrics(self):
        tasks = self._cmd("XLEN stream:rent:tasks")
        results = self._cmd("XLEN stream:rent:results")
        pending = self._cmd("XPENDING stream:rent:tasks workers")
        logs = self._logs()

        return {
            "tasks": int(tasks),
            "results": int(results),
            "pending": pending,
            "logs": logs
        }

    def _cmd(self, cmd):
        return subprocess.getoutput(f"{self.redis} {cmd}")

    def _logs(self):
        return subprocess.getoutput(
            "docker logs --tail 50 lentra-worker-stream"
        )

    # -----------------------------
    # ANALYSIS ENGINE
    # -----------------------------
    def analyze(self, m):
        tasks = m["tasks"]
        results = m["results"]
        logs = m["logs"]

        # 1. Worker crash / import error
        if "ImportError" in logs:
            return {
                "root_cause": "WORKER_IMPORT_FAILURE",
                "severity": "CRITICAL",
                "reason": "Python module import mismatch or broken lifecycle module",
                "action": "fix_imports_and_rebuild_worker"
            }

        # 2. Execution failure inside process()
        if "Invalid input of type: 'dict'" in logs:
            return {
                "root_cause": "SERIALIZATION_FAILURE",
                "severity": "HIGH",
                "reason": "Redis XADD received dict instead of flat fields",
                "action": "fix_result_serialization_layer"
            }

        # 3. Tasks stuck
        if tasks > 0 and results == 0:
            return {
                "root_cause": "PIPELINE_EXECUTION_STUCK",
                "severity": "HIGH",
                "reason": "Worker consumes tasks but does not produce results",
                "action": "inspect_worker_process_flow"
            }

        # 4. Idle system
        if tasks == 0:
            return {
                "root_cause": "SYSTEM_IDLE",
                "severity": "INFO",
                "reason": "No incoming workload",
                "action": "no_action_required"
            }

        return {
            "root_cause": "UNKNOWN_STATE",
            "severity": "MEDIUM",
            "reason": "No matching failure pattern",
            "action": "manual_inspection_required"
        }

    # -----------------------------
    # ENTRYPOINT
    # -----------------------------
    def run(self):
        metrics = self.collect_metrics()
        result = self.analyze(metrics)

        print(json.dumps({
            "metrics": metrics,
            "diagnosis": result
        }, indent=2))


if __name__ == "__main__":
    RootCauseEngine().run()
