class ScenarioRegistry:

    def __init__(self):
        self._scenarios = {}

    def register(self, name, handler):
        self._scenarios[name] = handler

    def get(self, name):
        return self._scenarios.get(name)

    def all(self):
        return self._scenarios


scenario_registry = ScenarioRegistry()
