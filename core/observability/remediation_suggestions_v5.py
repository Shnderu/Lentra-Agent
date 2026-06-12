"""
Lentra Observable Core v5
Remediation Suggestion Layer
"""


class RemediationSuggestions:

    def suggest(self, decision):
        action = decision.get("action")

        suggestions = []

        if action == "SCALE_WORKERS":
            suggestions.append("Increase worker replicas by 2-3 instances")
            suggestions.append("Check queue consumer lag")

        elif action == "ALERT_SRE":
            suggestions.append("Trigger on-call alert")
            suggestions.append("Dump observability report (v4)")

        elif action == "MONITOR":
            suggestions.append("Increase monitoring frequency")
            suggestions.append("Track lag trend slope")

        elif action == "NOOP":
            suggestions.append("No action required")

        return {
            "action": action,
            "suggestions": suggestions
        }


if __name__ == "__main__":
    import json

    s = RemediationSuggestions()
    print(json.dumps(s.suggest({"action": "SCALE_WORKERS"}), indent=2))
