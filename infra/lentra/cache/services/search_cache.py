# ============================================================
# SEARCH CACHE SERVICE V16.7
# ============================================================

from lentra.cache.storage.memory import MemoryCache
from lentra.cache.services.key_builder import build_search_key


class SearchCacheService:
    def __init__(self):
        self.cache = MemoryCache()

    def get(self, query):
        key = build_search_key(query)
        return self.cache.get(key)

    def set(self, query, value):
        key = build_search_key(query)
        self.cache.set(key, value, ttl=120)
