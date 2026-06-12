import json
from core.observability.incident_classifier_v5 import IncidentClassifier
from core.observability.policy_engine_v5 import PolicyEngine

"""
Lentra Observable Core v5
Autonomous Incident Manager
"""


class IncidentManager:

    def run(self):
        classifier = IncidentClassifier()
        policy = PolicyEngine()

        incident = classifier.classify()
        decision = policy.evaluate(incident)

        return {
            "incident": incident,
            "decision": decision
        }


if __name__ == "__main__":
    m = IncidentManager()
    print(json.dumps(m.run(), indent=2))
