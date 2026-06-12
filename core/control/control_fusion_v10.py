from core.control.control_brain_v10 import ControlBrain
from core.control.policy_engine_v10 import PolicyEngine

"""
Lentra Control Fusion v10
Unified Decision System (Safe Mode)
"""


class ControlFusion:

    def run(self, prediction: dict):

        brain = ControlBrain()
        policy = PolicyEngine()

        decision = brain.evaluate(prediction)
        policy_result = policy.validate(decision["actions"])

        return {
            "decision": decision,
            "policy": policy_result,
            "final_state": "ADVISORY_CONTROL_MODE"
        }


if __name__ == "__main__":
    import json

    test = {
        "risk": {"risk_score": 85, "level": "CRITICAL"},
        "failure_signals": {"pre_failure": True}
    }

    print(json.dumps(ControlFusion().run(test), indent=2))
