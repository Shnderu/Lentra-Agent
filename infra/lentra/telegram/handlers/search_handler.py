from lentra.core.market_intelligence.search.nlp.query_parser import QueryParser

class SearchHandler:

    def __init__(self, engine):
        self.engine = engine
        self.parser = QueryParser()

    def handle(self, text: str):

        query = self.parser.parse(text)

        listings = self._mock_listings()

        results = self.engine.analyze(listings, query_text=text)

        return results

    def _mock_listings(self):
        return [
            {"title": "Studio near beach", "price": 700, "location": "da nang beach"},
            {"title": "Cheap room center", "price": 200, "location": "da nang center"},
        ]
