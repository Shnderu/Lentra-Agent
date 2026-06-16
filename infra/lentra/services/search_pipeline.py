class SearchPipeline:
    """
    STABLE COMPATIBILITY LAYER

    Fixes mismatch between:
    - handlers expecting search_service
    - legacy pipelines expecting state_store/cache/fsm
    """

    def __init__(
        self,
        search_service=None,
        state_store=None,
        fsm=None,
        cache=None,
        renderer=None,
        **kwargs
    ):
        self.search_service = search_service
        self.state_store = state_store
        self.fsm = fsm
        self.cache = cache
        self.renderer = renderer

    async def run(self, query: str, user_id: int = None):
        """
        Unified safe entrypoint
        """

        # fallback search
        if self.search_service:
            try:
                return await self.search_service.search(query)
            except Exception:
                return []

        return []
