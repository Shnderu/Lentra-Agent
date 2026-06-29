class IntentRouter:

    def route(self, request: dict):

        intent = {
            "name": request.get("intent", "unknown"),
            "confidence": request.get("confidence", 0.3),
            "payload": request,
            "scenarios": ["default_scenario_v1"]
        }

        return intent
