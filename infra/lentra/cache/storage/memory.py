# ============================================================
# LENTRA CACHE STORAGE V16.7
# ============================================================

import time


class MemoryCache:
    def __init__(self):
        self.store = {}

    def set(self, key, value, ttl=60):
        self.store[key] = {
            "value": value,
            "expires": time.time() + ttl
        }

    def get(self, key):
        item = self.store.get(key)

        if not item:
            return None

        if time.time() > item["expires"]:
            del self.store[key]
            return None

        return item["value"]
