import json
from core.observability.failure_probability_graph_v3 import FailureProbabilityGraph
from core.observability.anomaly_forecaster_v3 import AnomalyForecaster
from core.observability.pre_failure_detector_v3 import PreFailureDetector

"""
Lentra Observable Core v3
Predictive Health Layer
"""


def predictive_health():
    graph = FailureProbabilityGraph()
    forecaster = AnomalyForecaster()
    detector = PreFailureDetector()

    risk_graph = graph.compute_risk()
    anomaly = forecaster.forecast_lag_risk()
    pre_fail = detector.detect()

    overall_risk = "LOW"

    if anomaly["risk_level"] == "HIGH" or pre_fail["risk"] == "HIGH":
        overall_risk = "HIGH"
    elif anomaly["risk_level"] == "MEDIUM":
        overall_risk = "MEDIUM"

    return {
        "overall_risk": overall_risk,
        "graph_risk": risk_graph,
        "anomaly": anomaly,
        "pre_failure": pre_fail
    }


if __name__ == "__main__":
    print(json.dumps(predictive_health(), indent=2))
