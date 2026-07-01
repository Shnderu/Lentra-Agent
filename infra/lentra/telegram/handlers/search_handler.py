from lentra.runtime.intelligence_gateway import interpret


class SearchHandler:

    def __init__(self, engine):
        self.engine = engine

    def handle(self, listings, text):
        payload = {
            "task": "search",
            "listings": listings,
            "query": text
        }

        # CANONICAL ENTRY
        return interpret(payload)
