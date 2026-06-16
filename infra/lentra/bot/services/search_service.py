import os


class SearchService:

    def __init__(self, api_url: str):
        self.api_url = api_url

    async def search(self, query: str):
        # временный stub (стабилизация)
        return []
