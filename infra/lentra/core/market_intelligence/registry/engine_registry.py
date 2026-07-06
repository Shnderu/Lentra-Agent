from dataclasses import dataclass
from typing import Dict, Any


@dataclass(frozen=True)
class EngineSpec:
    name: str
    version: str
    required: bool = True


class EngineRegistry:
    """
    IMMUTABLE ENGINE REGISTRY

    RULES:
    - NO dynamic discovery
    - NO runtime injection
    - version-locked execution
    """

    def __init__(self):
        self._engines = {
            "signals": EngineSpec(name="signals", version="v1"),
            "risk": EngineSpec(name="risk", version="v1"),
            "ranking": EngineSpec(name="ranking", version="v2"),
            "enrichment": EngineSpec(name="enrichment", version="v2"),
        }

    def get(self, name: str) -> EngineSpec:
        if name not in self._engines:
            raise ValueError(f"Engine not registered: {name}")
        return self._engines[name]

    def resolve(self, name: str) -> EngineSpec:
        return self.get(name)

    def list(self):
        return {
            k: {
                "name": v.name,
                "version": v.version,
                "required": v.required
            }
            for k, v in self._engines.items()
        }

    def keys(self):
        return list(self._engines.keys())
