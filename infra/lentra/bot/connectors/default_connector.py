class DefaultConnector:
    def search(self, query: dict):
        return {
            "source": "default_connector",
            "query": query,
            "items": []
        }

    def fetch(self, query: dict):
        return self.search(query)

    def call(self, query: dict):
        return self.search(query)
