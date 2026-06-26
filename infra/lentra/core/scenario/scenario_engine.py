class ScenarioEngine:
    def __init__(self, registry):
        self.registry = registry

    def run(self, intent: str, context: dict):
        # canonical execution contract (LOCKED)
        return self.registry.execute(intent, context)


def build_scenario_engine(registry):
    return ScenarioEngine(registry)
