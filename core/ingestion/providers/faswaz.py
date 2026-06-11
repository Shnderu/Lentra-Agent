from core.ingestion.providers.base import BaseProvider
from core.domain import RentQuery, RentListing


class FaswazProvider(BaseProvider):
    name = "faswaz"
    rate_limit = 1.0

    def fetch(self, query: RentQuery):
        return [
            RentListing(
                title=f"Faswaz Villa in {query.city}",
                price=(query.budget or 800) - 100,
                currency="USD",
                location=query.city,
                source=self.name,
                url="https://faswaz.com/mock"
            )
        ]
