from typing import Dict, Any


class FrozenContext:
    """
    IMMUTABLE SNAPSHOT CONTEXT

    RULES:
    - no mutation allowed
    - each update returns NEW instance
    - supports event-sourcing style pipeline
    """

    def __init__(self, data: Dict[str, Any]):
        # internal immutable snapshot
        self._data = self._deep_freeze(data)

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def as_dict(self) -> Dict[str, Any]:
        return self._data

    def update(self, patch: Dict[str, Any]) -> "FrozenContext":
        merged = {
            **self._data,
            **patch
        }
        return FrozenContext(merged)

    def _deep_freeze(self, obj):
        """
        lightweight immutability enforcement
        (no recursion-heavy overhead for MVP)
        """
        if isinstance(obj, dict):
            return {k: self._deep_freeze(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return tuple(self._deep_freeze(v) for v in obj)
        return obj
