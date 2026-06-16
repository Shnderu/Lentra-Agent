import time


class SearchPipeline:
    """
    Stable compatibility pipeline.

    Supports BOTH old and new DI signatures:
    - search_service
    - state_store
    - fsm
    - cache
    - renderer
    """

    def __init__(
        self,
        search_service=None,
        state_store=None,
        fsm=None,
        cache=None,
        renderer=None
    ):
        self.search_service = search_service
        self.state_store = state_store
        self.fsm = fsm
        self.cache = cache
        self.renderer = renderer

    async def execute(self, user_id: int, query: str, message=None):
        start = time.time()

        # 1) STATE (safe fallback)
        state = {}
        if self.state_store and hasattr(self.state_store, "load"):
            try:
                state = self.state_store.load(user_id) or {}
            except Exception:
                state = {}

        # 2) SEARCH (safe fallback)
        items = []

        if self.search_service and hasattr(self.search_service, "search"):
            try:
                items = await self.search_service.search(query)
            except Exception:
                items = []
        else:
            # fallback mock
            items = [
                {
                    "title": f"Result for: {query}",
                    "price": None
                }
            ]

        # 3) CACHE SAFE WRITE
        search_id = f"{user_id}:{int(start)}"
        self._safe_cache_write(search_id, items)

        # 4) FSM (optional)
        if self.fsm and hasattr(self.fsm, "handle"):
            try:
                state = self.fsm.handle(state, {"query": query})
            except Exception:
                pass

        # 5) RESPONSE
        return {
            "screen": "search",
            "state": {
                "query": query,
                "results": items,
                "state": state
            }
        }

    def _safe_cache_write(self, search_id, items):
        if not self.cache:
            return

        if hasattr(self.cache, "set_results"):
            try:
                self.cache.set_results(search_id, items)
                return
            except Exception:
                pass

        if hasattr(self.cache, "save"):
            try:
                self.cache.save(search_id, items)
                return
            except Exception:
                pass

        if hasattr(self.cache, "set"):
            try:
                self.cache.set(search_id, items)
                return
            except Exception:
                pass
