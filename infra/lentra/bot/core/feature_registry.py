from typing import Callable, Dict, Any


class FeatureRegistry:
    """
    Production registry for features.
    """

    def __init__(self):
        self._features: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register(self, name: str, handler: Callable):
        self._features[name] = handler

    def get(self, name: str):
        return self._features.get(name)

    def has(self, name: str) -> bool:
        return name in self._features
