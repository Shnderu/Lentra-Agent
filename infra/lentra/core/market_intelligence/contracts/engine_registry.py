from typing import Dict, Any


class EngineRegistry:
    """
    CENTRAL ENGINE REGISTRY
    prevents direct cross-import chaos
    """

    def __init__(self):
        self._engines: Dict[str, Any] = {}

    def register(self, name: str, engine: Any):
        self._engines[name] = engine

    def get(self, name: str):
        return self._engines.get(name)

    def resolve(self, name: str):
        return self.get(name)

    def all(self):
        return self._engines
