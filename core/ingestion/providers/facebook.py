from core.ingestion.providers.base import BaseProvider
from core.domain import RentQuery, RentListing


class FacebookProvider(BaseProvider):
    name = "facebook"
    rate_limit = 1.5

    def fetch(self, query: RentQuery):
        return [
            RentListing(
                title=f"FB Apartment in {query.city}",
                price=query.budget or 500,
                currency="USD",
                location=query.city,
                source=self.name,
                url="https://facebook.com/mock"
            )
        ]
