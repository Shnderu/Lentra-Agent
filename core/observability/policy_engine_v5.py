"""
Lentra Observable Core v5
Policy Engine (rule-based remediation suggestions)
"""


class PolicyEngine:

    def evaluate(self, incident):
        severity = incident.get("severity")

        if severity == "NONE":
            return {
                "action": "NOOP",
                "reason": "System healthy"
            }

        if severity == "LOW":
            return {
                "action": "MONITOR",
                "reason": "Minor lag detected"
            }

        if severity == "MEDIUM":
            return {
                "action": "SCALE_WORKERS",
                "reason": "Backlog building up"
            }

        if severity == "HIGH":
            return {
                "action": "ALERT_SRE",
                "reason": "Critical backlog detected"
            }

        return {
            "action": "UNKNOWN",
            "reason": "Unclassified state"
        }


if __name__ == "__main__":
    import json

    p = PolicyEngine()
    print(json.dumps(p.evaluate({"severity": "MEDIUM"}), indent=2))
