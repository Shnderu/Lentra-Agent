from typing import Callable, Dict
from lentra.bot.features.base.context import FeatureContext


class FeatureRegistry:
    """
    Simple in-memory feature registry (production baseline).
    """

    def __init__(self):
        self._features: Dict[str, Callable[[FeatureContext], str]] = {}

    def register(self, name: str, handler: Callable):
        self._features[name] = handler

    def get(self, name: str):
        return self._features.get(name)
