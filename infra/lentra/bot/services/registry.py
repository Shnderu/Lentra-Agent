import os
from lentra.bot.state.state_store import StateStore
from lentra.bot.services.search_service import SearchService


class Registry:
    """
    PURE RUNTIME REGISTRY (NO FACTORIES, NO DI GRAPH)
    """

    def __init__(self):
        self.state_store = StateStore()

        # TEMP: real search service stub binding
        self.search_service = SearchService(
            api_url=os.getenv("SEARCH_API_URL", "http://localhost:8000")
        )
