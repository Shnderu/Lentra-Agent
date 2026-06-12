import json
from core.observability.incident_manager_v5 import IncidentManager
from core.observability.remediation_suggestions_v5 import RemediationSuggestions

"""
Lentra Observable Core v5
Incident Autopilot (SAFE MODE)
"""


class IncidentAutopilot:

    def run(self):
        manager = IncidentManager()
        suggester = RemediationSuggestions()

        result = manager.run()
        suggestions = suggester.suggest(result["decision"])

        return {
            "incident": result["incident"],
            "decision": result["decision"],
            "remediation": suggestions
        }


if __name__ == "__main__":
    a = IncidentAutopilot()
    print(json.dumps(a.run(), indent=2))
