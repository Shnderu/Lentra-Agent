from typing import Callable, Dict, Any


class ScenarioRegistry:
    def __init__(self):
        self._scenarios: Dict[str, Any] = {}

    def register(self, name: str, handler: Callable):
        """
        Registry stores execution-compatible handlers.
        If plain function is passed — wrap it into .execute() adapter.
        """

        if hasattr(handler, "execute"):
            self._scenarios[name] = handler
            return

        class FunctionAdapter:
            def __init__(self, fn):
                self.fn = fn

            def execute(self, state: dict):
                return self.fn(state)

        self._scenarios[name] = FunctionAdapter(handler)

    def get(self, name: str):
        return self._scenarios.get(name)

    def all(self):
        return self._scenarios


scenario_registry = ScenarioRegistry()
