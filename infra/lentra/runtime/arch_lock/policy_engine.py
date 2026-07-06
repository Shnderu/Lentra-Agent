from typing import List, Dict


class PolicyEngine:
    """
    ARCH LOCK v1.6 Policy Engine
    Pure rule evaluation layer
    """

    def __init__(self, rules: List[Dict]):
        self.rules = rules

    def evaluate(self, violations):
        if not violations:
            return {"status": "OK", "score": 1.0}

        score = max(0.0, 1.0 - (len(violations) * 0.2))

        return {
            "status": "FAIL" if violations else "OK",
            "score": score,
            "violations": violations
        }
