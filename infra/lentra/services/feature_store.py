from typing import Dict, Any, List

class FeatureStore:
    """
    In-memory feature cache for ranking stage.
    """

    def __init__(self):
        self._cache = {}

    def get(self, property_id: int) -> Dict[str, Any]:
        return self._cache.get(property_id, {})

    def bulk_get(self, ids: List[int]) -> Dict[int, Dict[str, Any]]:
        return {i: self._cache.get(i, {}) for i in ids}

    def set(self, property_id: int, features: Dict[str, Any]):
        self._cache[property_id] = features

    def update_many(self, items: Dict[int, Dict[str, Any]]):
        for k, v in items.items():
            self._cache[k] = v
