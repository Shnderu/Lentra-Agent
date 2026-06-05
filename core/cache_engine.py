import time
from typing import Any, Optional


class CacheEngine:
    """
    v2.7 Cache Pro (memory-based, production-ready interface)
    """

    def __init__(self):
        self._store = {}
        self._ttl = {}

    def set(self, key: str, value: Any, ttl: int = None):
        self._store[key] = value

        if ttl:
            self._ttl[key] = time.time() + ttl

    def get(self, key: str) -> Optional[Any]:
        if key not in self._store:
            return None

        # TTL check
        if key in self._ttl:
            if time.time() > self._ttl[key]:
                self._delete_internal(key)
                return None

        return self._store[key]

    def delete(self, key: str):
        self._delete_internal(key)

    def clear(self):
        self._store.clear()
        self._ttl.clear()

    def _delete_internal(self, key: str):
        self._store.pop(key, None)
        self._ttl.pop(key, None)


# SINGLETON (важно для всего проекта)
cache = CacheEngine()
