from typing import Dict, Any, List
import threading


class FeatureStore:
    """
    In-memory feature cache.
    Сейчас: простая RAM-структура.
    Позже: можно заменить на Redis без изменения API слоя.
    """

    def __init__(self):
        self._lock = threading.RLock()
        self._features: Dict[int, Dict[str, Any]] = {}

    def set(self, property_id: int, features: Dict[str, Any]):
        with self._lock:
            self._features[property_id] = features

    def get(self, property_id: int) -> Dict[str, Any]:
        return self._features.get(property_id, {})

    def bulk_set(self, items: List[Dict[str, Any]]):
        """
        items: [{"id": 1, "features": {...}}, ...]
        """
        with self._lock:
            for item in items:
                self._features[item["id"]] = item.get("features", {})

    def all(self) -> Dict[int, Dict[str, Any]]:
        return self._features

    def clear(self):
        with self._lock:
            self._features.clear()


# Singleton
feature_store = FeatureStore()
