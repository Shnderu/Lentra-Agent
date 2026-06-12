import redis
import json
from collections import defaultdict

class RootCauseEngine:
    def __init__(self, redis_host="lentra-redis"):
        self.r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

    def fetch_trace(self, limit=200):
        data = self.r.xrevrange("stream:rent:trace", count=limit)
        return data

    def build_chain(self, trace):
        chain = defaultdict(list)

        for msg_id, fields in trace:
            task_id = fields.get("task_id", "unknown")
            stage = fields.get("stage", "unknown")
            error = fields.get("error", "")

            chain[task_id].append({
                "stage": stage,
                "error": error,
                "raw": fields
            })

        return chain

    def analyze_task(self, events):
        stages = [e["stage"] for e in events]
        errors = [e["error"] for e in events if e["error"]]

        # RULE 1: ingestion OK but no PROCESS_START
        if "READ" in stages and "PROCESS_START" not in stages:
            return {
                "root_cause": "WORKER_EXECUTION_BLOCK",
                "stage": "PROCESS_START",
                "reason": "Task read but never entered processing layer",
                "severity": "critical"
            }

        # RULE 2: process starts but no results
        if "PROCESS_START" in stages and "RESULTS_WRITTEN" not in stages:
            return {
                "root_cause": "PROCESSING_FAILURE",
                "stage": "process()",
                "reason": "Execution started but never reached result emission",
                "severity": "critical"
            }

        # RULE 3: explicit errors
        if errors:
            return {
                "root_cause": "RUNTIME_EXCEPTION",
                "stage": stages[-1] if stages else "unknown",
                "reason": errors[-1],
                "severity": "high"
            }

        # RULE 4: healthy
        return {
            "root_cause": "OK",
            "stage": "complete",
            "reason": "Pipeline executed successfully",
            "severity": "none"
        }

    def analyze(self):
        trace = self.fetch_trace()
        chains = self.build_chain(trace)

        report = {}

        for task_id, events in chains.items():
            report[task_id] = self.analyze_task(events)

        return report


if __name__ == "__main__":
    engine = RootCauseEngine()
    report = engine.analyze()

    print(json.dumps(report, indent=2))
