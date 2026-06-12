from core.predictive.risk_engine_v9 import RiskEngine
from core.predictive.failure_signature_v9 import FailureSignature

"""
Lentra Predictive Core v9
Unified Prediction Layer
"""


class IncidentPredictor:

    def run(self, incident: dict, metrics: dict):

        risk = RiskEngine().compute_risk(incident)
        failure = FailureSignature().detect(metrics)

        return {
            "risk": risk,
            "failure_signals": failure,
            "early_warning": risk["level"] in ["WARNING", "CRITICAL"] or failure["pre_failure"]
        }


if __name__ == "__main__":
    predictor = IncidentPredictor()

    print(predictor.run(
        {
            "severity": "MEDIUM",
            "graph_size": 12,
            "edges": 15,
            "is_recurrent": True
        },
        {
            "queue_lag": 7,
            "error_rate": 0.25,
            "retry_rate": 0.4,
            "memory_spike": True
        }
    ))
