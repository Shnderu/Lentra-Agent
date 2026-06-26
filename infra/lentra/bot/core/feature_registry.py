from typing import Callable, Dict, Optional
from lentra.bot.features.base.context import FeatureContext


class FeatureRegistry:
    """
    Single source of truth registry.
    Must exist ONLY inside Container.
    """

    def __init__(self):
        self._features: Dict[str, Callable[[FeatureContext], str]] = {}

    def register(self, name: str, handler: Callable[[FeatureContext], str]) -> None:
        self._features[name] = handler

    def get(self, name: str) -> Optional[Callable[[FeatureContext], str]]:
        return self._features.get(name)

    def all(self) -> Dict[str, Callable]:
        return self._features
