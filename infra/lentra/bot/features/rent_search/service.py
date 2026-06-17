class RentSearchService:
    def __init__(self, connectors, trace=None):
        self.connectors = connectors
        self.trace = trace

    async def search(self, query: dict):

        if self.trace:
            self.trace.node("rent_search_start", query)

        results = []

        for c in self.connectors:

            if self.trace:
                self.trace.node("connector_call", {
                    "connector": c.__class__.__name__
                })

            data = c.fetch(query)

            if self.trace:
                self.trace.node("connector_result", data)

            results.append(data)

        if self.trace:
            self.trace.node("rent_search_end", {"items": len(results)})

        return {
            "text": "rent_search v3",
            "raw": results,
            "trace_id": self.trace.trace_id if self.trace else None
        }
