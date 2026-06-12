import json
import time
from core.healing.stability_layer_v2 import StabilityLayerV2


class SafeAIAdvisorV2:
    """
    SAFE AI ADVISOR v2

    RULES:
    - NEVER execute fixes
    - NEVER restart services
    - ONLY produce suggestions
    """

    def __init__(self):
        self.layer = StabilityLayerV2()

    def analyze(self):
        report = self.layer.diagnose()

        suggestions = []

        if "REDIS_UNREACHABLE_OR_TIMEOUT" in report["root_causes"]:
            suggestions.append("Check docker network (infra_default) and redis hostname resolution")

        if "SERVICE_DISCOVERY_FAILURE" in report["root_causes"]:
            suggestions.append("Fix container DNS resolution or attach worker to same network as redis")

        if "PIPELINE_BACKPRESSURE_OR_WORKER_LAG" in report["root_causes"]:
            suggestions.append("Inspect XREADGROUP consumer lag and worker ack flow")

        if not suggestions:
            suggestions.append("System healthy — no actions required")

        return {
            "status": "SAFE_AI_ADVISOR_V2",
            "analysis": report,
            "suggested_fixes": suggestions,
            "auto_apply": False,
            "risk_level": "CONTROLLED"
        }


if __name__ == "__main__":
    advisor = SafeAIAdvisorV2()
    print(json.dumps(advisor.analyze(), indent=2))
