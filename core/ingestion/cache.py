import json
import time


class IngestionCache:
    def __init__(self, ttl: int = 300):
        self.ttl = ttl
        self.store = {}

    def _expired(self, key: str) -> bool:
        if key not in self.store:
            return True
        return time.time() > self.store[key]["expires_at"]

    def get(self, key: str):
        if self._expired(key):
            return None
        return self.store[key]["value"]

    def set(self, key: str, value):
        self.store[key] = {
            "value": value,
            "expires_at": time.time() + self.ttl
        }
