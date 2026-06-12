import json
from core.diagnostics.root_cause_engine import RootCauseEngine

class ReasoningEngine:

    def __init__(self):
        self.rc = RootCauseEngine()

    # -----------------------------
    # HUMAN EXPLANATION LAYER
    # -----------------------------
    def explain(self, diagnosis):
        rc = diagnosis["root_cause"]

        explanations = {
            "WORKER_IMPORT_FAILURE": 
                "Worker crashes due to broken Python imports or inconsistent module state. System cannot start execution loop.",

            "SERIALIZATION_FAILURE":
                "Data sent to Redis XADD is not properly serialized. Worker produces structured dict instead of flat fields.",

            "PIPELINE_EXECUTION_STUCK":
                "Tasks are consumed but no results are produced. Execution pipeline is broken between processing and output stage.",

            "SYSTEM_IDLE":
                "No tasks in the system. Execution layer is healthy but inactive.",

            "UNKNOWN_STATE":
                "System state does not match known failure patterns. Manual inspection required."
        }

        return explanations.get(rc, "No explanation available for this state.")

    # -----------------------------
    # PREDICTIVE ANALYSIS (heuristic v1)
    # -----------------------------
    def predict(self, metrics):
        tasks = metrics["tasks"]
        results = metrics["results"]

        # trend-based heuristics
        if tasks > 10 and results == 0:
            return {
                "risk": "HIGH",
                "prediction": "Pipeline backlog will grow and cause worker saturation"
            }

        if tasks > 0 and results > 0:
            return {
                "risk": "LOW",
                "prediction": "System stable with normal throughput"
            }

        return {
            "risk": "MEDIUM",
            "prediction": "Insufficient data for strong prediction"
        }

    # -----------------------------
    # CONFIG OPTIMIZATION SUGGESTIONS
    # -----------------------------
    def recommend(self, diagnosis):
        rc = diagnosis["root_cause"]

        if rc == "PIPELINE_EXECUTION_STUCK":
            return [
                "Increase worker concurrency",
                "Add retry backoff tuning",
                "Check serialization layer before Redis XADD"
            ]

        if rc == "WORKER_IMPORT_FAILURE":
            return [
                "Pin dependency versions",
                "Rebuild docker image",
                "Validate module imports at startup"
            ]

        return ["No optimization required"]

    # -----------------------------
    # ENTRYPOINT
    # -----------------------------
    def run(self):
        metrics = self.rc.collect_metrics()
        diagnosis = self.rc.analyze(metrics)

        result = {
            "diagnosis": diagnosis,
            "explanation": self.explain(diagnosis),
            "prediction": self.predict(metrics),
            "recommendations": self.recommend(diagnosis)
        }

        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    ReasoningEngine().run()
