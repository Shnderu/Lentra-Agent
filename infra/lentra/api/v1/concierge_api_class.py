

from lentra.core.pipeline.pipeline import LentraPipeline


class ConciergeAPIv1:

    def __init__(self):
        self.pipeline = LentraPipeline()

    def search(self, query: str):

        raw_listing = {
            "id": "api-1",
            "title": query,
            "price": 600,
            "market_avg": 550,
            "currency": "USD",
            "city": "Da Nang",
            "location": "My My",
            "source": "api"
        }

        return self.pipeline.run(raw_listing)
