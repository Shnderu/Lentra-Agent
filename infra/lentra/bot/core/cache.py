class ResultCache:
    def __init__(self, redis=None):
        self.redis = redis
        self._mem = {}

    def set(self, key, value):
        self._mem[key] = value

    def get(self, key):
        return self._mem.get(key)

    # === FIX COMPAT LAYER ===
    def set_results(self, search_id, items):
        """
        Legacy compatibility for search_pipeline
        """
        self._mem[search_id] = items

    def get_results(self, search_id):
        return self._mem.get(search_id, [])
