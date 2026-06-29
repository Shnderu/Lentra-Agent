class ScenarioRegistry:
    def __init__(self):
        self._scenarios = {}

    def register(self, name: str, scenario):
        self._scenarios[name] = scenario

    def get(self, name: str):
        return self._scenarios.get(name)

    def list(self):
        return list(self._scenarios.keys())


# SINGLETON REGISTRY (critical fix)
scenario_registry = ScenarioRegistry()
