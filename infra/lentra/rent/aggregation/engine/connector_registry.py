class ConnectorRegistry:
    """
    Хранит список источников данных
    """

    def __init__(self):
        self.connectors = []

    def register(self, connector):
        self.connectors.append(connector)

    async def fanout(self, query: dict):
        results = []

        for c in self.connectors:
            try:
                r = await c.call(query)
                results.append(r)
            except Exception:
                continue

        return results
