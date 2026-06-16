from typing import Dict, Any, Callable


class FeatureRegistry:
    """
    Центральный реестр фичей.
    Управляет подключением feature-сервисов к системе.
    """

    def __init__(self):
        self._features: Dict[str, Any] = {}

    def register(self, name: str, feature: Any) -> None:
        self._features[name] = feature

    def get(self, name: str) -> Any:
        return self._features.get(name)

    def has(self, name: str) -> bool:
        return name in self._features

    def all(self) -> Dict[str, Any]:
        return self._features
