class DefaultConnector:

    def __init__(self):
        # можно позже добавить API/HTTP/DB
        pass

    async def call(self, query: dict) -> dict:

        # STABLE MOCK CONTRACT
        return {
            "source": "default_connector",
            "query": query,
            "items": []   # пока без данных
        }
