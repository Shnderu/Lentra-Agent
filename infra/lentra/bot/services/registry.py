import os

from lentra.bot.state.state_store import StateStore
from lentra.bot.services.search_pipeline import SearchService


class SearchServiceFactory:

    @staticmethod
    def create():
        api_url = os.getenv("SEARCH_API_URL", "http://localhost:8000")
        return SearchService(api_url=api_url)


class Registry:

    def __init__(self):
        self.search_service = SearchServiceFactory.create()
        self.state_store = StateStore()
