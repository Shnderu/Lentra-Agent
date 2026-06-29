from lentra.core.scenario.runtime_adapter import ScenarioAdapter


class ScenarioRegistry:
    def __init__(self):
        self._scenarios = {}

    def register(self, name: str, fn):
        # всегда оборачиваем в адаптер
        self._scenarios[name] = ScenarioAdapter(fn)

    def get(self, name: str):
        return self._scenarios.get(name)

    def all(self):
        return self._scenarios


scenario_registry = ScenarioRegistry()
