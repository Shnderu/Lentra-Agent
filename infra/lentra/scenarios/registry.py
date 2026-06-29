class ScenarioRegistry:
    """
    Minimal stable registry.
    Avoid circular imports. No scenario auto-loading here.
    """

    def __init__(self):
        self._scenarios = {}

    def register(self, name: str, scenario):
        self._scenarios[name] = scenario

    def get(self, name: str):
        return self._scenarios.get(name)

    def list(self):
        return list(self._scenarios.keys())


# single instance (IMPORTANT: no function factory, no DI recursion)
scenario_registry = ScenarioRegistry()
