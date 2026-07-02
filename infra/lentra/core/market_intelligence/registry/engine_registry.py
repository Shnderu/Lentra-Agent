from typing import Dict, Any


class EngineRegistryV2:
    """
    STRICT ENGINE INSTANCE REGISTRY

    RULES:
    - stores ENGINE OBJECTS only
    - NEVER stores evaluation results
    """

    def __init__(self, engines: Dict[str, Any]):
        self._engines = {}

        for name, engine in engines.items():
            if hasattr(engine, "evaluate"):
                self._engines[name] = engine

    def get(self, name: str):
        return self._engines.get(name)

    def all(self):
        return self._engines

    def names(self):
        return list(self._engines.keys())
