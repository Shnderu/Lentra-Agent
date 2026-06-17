class DefaultConnector:
    async def call(self, query: dict) -> dict:
        return {
            "source": "default_connector",
            "query": query,
            "items": []
        }
