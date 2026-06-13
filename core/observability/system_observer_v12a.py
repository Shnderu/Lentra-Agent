"""
Lentra Observability Control Plane v12a
Single unified system state viewer
"""

from core.fusion.incident_intelligence_v7 import IncidentFusionEngine
from core.memory.incident_memory_fusion_v8 import MemoryFusion
from core.predictive.predictor_v9 import Predictor
from core.control.control_fusion_v10 import ControlFusion
from core.schema.event_validator_v11 import EventValidator


class SystemObserver:

    def __init__(self):
        self.fusion = IncidentFusionEngine()
        self.memory = MemoryFusion()
        self.predictor = Predictor()
        self.control = ControlFusion()
        self.validator = EventValidator()

    def snapshot(self, event: dict):

        # v11 validation layer
        validation = self.validator.validate(event)

        # v7
        fusion_state = self.fusion.run()

        # v8
        memory_state = self.memory.run(event)

        # v9
        prediction_state = self.predictor.run()

        # v10
        control_state = self.control.run(prediction_state)

        return {
            "schema": validation,
            "fusion_v7": fusion_state,
            "memory_v8": memory_state,
            "prediction_v9": prediction_state,
            "control_v10": control_state,
            "system_health": self._health_score(
                fusion_state,
                memory_state,
                prediction_state
            )
        }

    def _health_score(self, fusion, memory, prediction):

        score = 100

        if prediction.get("risk", {}).get("risk_score", 0) > 80:
            score -= 40

        if memory.get("is_recurrent"):
            score -= 20

        if fusion.get("fusion", {}).get("severity") != "NONE":
            score -= 10

        return max(0, score)


if __name__ == "__main__":
    observer = SystemObserver()

    test_event = {
        "type": "rent.search",
        "severity": "HIGH",
        "graph_size": 8,
        "edges": 5,
        "payload": {"city": "Phu Quoc"}
    }

    import json
    print(json.dumps(observer.snapshot(test_event), indent=2))
