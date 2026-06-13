"""
Lentra Full Stack Check v7-v12b
Single command system integrity test
"""

import json

from core.fusion.incident_intelligence_v7 import IncidentFusionEngine
from core.memory.incident_memory_fusion_v8 import MemoryFusion
from core.predictive.predictor_v9 import Predictor
from core.control.control_fusion_v10 import ControlFusion
from core.schema.event_validator_v11 import EventValidator
from core.observability.system_observer_v12a import SystemObserver


class FullStackCheck:

    def __init__(self):
        self.v7 = IncidentFusionEngine()
        self.v8 = MemoryFusion()
        self.v9 = Predictor()
        self.v10 = ControlFusion()
        self.v11 = EventValidator()
        self.v12 = SystemObserver()

    def run(self):

        test_event = {
            "type": "rent.search",
            "severity": "HIGH",
            "graph_size": "7",
            "edges": "5",
            "payload": {"city": "Phu Quoc"}
        }

        report = {}

        # v11 first (schema gate)
        report["v11"] = self.v11.validate(test_event)

        # v7
        report["v7"] = self.v7.run()

        # v8
        report["v8"] = self.v8.run(test_event)

        # v9
        report["v9"] = self.v9.run()

        # v10
        report["v10"] = self.v10.run(report["v9"])

        # v12a snapshot (full system view)
        report["v12a"] = self.v12.snapshot(test_event)

        # health summary
        report["health"] = self._health(report)

        return report

    def _health(self, report):

        score = 100

        if not report["v11"]["valid"]:
            score -= 30

        if report["v9"]["risk"]["risk_score"] > 80:
            score -= 30

        if report["v8"].get("is_recurrent"):
            score -= 20

        if report["v7"]["fusion"]["severity"] != "NONE":
            score -= 10

        return max(0, score)


if __name__ == "__main__":
    checker = FullStackCheck()
    print(json.dumps(checker.run(), indent=2))
