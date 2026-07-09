from typing import List, Dict


class PolicyEngine:
    """
    ARCH LOCK v1.6 Policy Engine

    Evaluates firewall scan result.
    """

    def __init__(self, rules: List[Dict]):
        self.rules = rules

    def evaluate(self, violations):

        if isinstance(violations, dict):

            status = violations.get(
                "status",
                "FAIL"
            )

            items = violations.get(
                "violations",
                []
            )

            if status == "OK" and not items:
                return {
                    "status": "OK",
                    "score": 1.0,
                    "violations": []
                }

            violations = items


        if not violations:
            return {
                "status": "OK",
                "score": 1.0,
                "violations": []
            }


        score = max(
            0.0,
            1.0 - (len(violations) * 0.2)
        )

        return {
            "status": "FAIL",
            "score": score,
            "violations": violations
        }
