import time


class SearchPipeline:
    """
    Minimal stable search pipeline.
    Works with any cache implementation safely.
    """

    def __init__(self, cache):
        self.cache = cache

    async def execute(self, user_id: int, query: str, message=None):
        start = time.time()

        # mock search result (если нет search service — система не падает)
        items = [
            {
                "title": f"Result for: {query}",
                "price": None
            }
        ]

        search_id = f"{user_id}:{int(start)}"

        # SAFE CACHE WRITE (no strict API dependency)
        self._safe_cache_write(search_id, items)

        return {
            "screen": "search",
            "state": {
                "query": query,
                "results": items
            }
        }

    def _safe_cache_write(self, search_id, items):
        """
        Works with any cache implementation.
        """
        if hasattr(self.cache, "set_results"):
            self.cache.set_results(search_id, items)
        elif hasattr(self.cache, "save"):
            self.cache.save(search_id, items)
        elif hasattr(self.cache, "set"):
            self.cache.set(search_id, items)
        else:
            # last fallback — no-op (system must not crash)
            return
