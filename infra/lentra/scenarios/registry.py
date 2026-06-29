import sys

class ScenarioRegistry:
    def __init__(self):
        self._store = {}

    def register(self, name, scenario):
        print(f"[REGISTRY] register -> {name}")
        self._store[name] = scenario

    def get(self, name):
        return self._store.get(name)

    def dump(self):
        return list(self._store.keys())


scenario_registry = ScenarioRegistry()

print("[REGISTRY INIT] id =", id(scenario_registry))
print("[REGISTRY INIT] module =", __name__)
print("[REGISTRY INIT] sys.modules key =", [k for k in sys.modules.keys() if "registry" in k])
