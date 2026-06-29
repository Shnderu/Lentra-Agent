class DefaultScenarioV1:
    def execute(self, payload):
        # FIX: поддержка ExecutionStateV1 и dict одновременно
        if hasattr(payload, "get"):
            query = payload.get("query", "")
        else:
            query = getattr(payload, "query", "")

        return {
            "entry": "default_scenario_v1",
            "query": query,
            "status": "ok"
        }


def run(payload):
    return DefaultScenarioV1().execute(payload)
