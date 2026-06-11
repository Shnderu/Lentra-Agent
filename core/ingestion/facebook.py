from typing import List
from core.ingestion.base import BaseIngestionSource
from core.domain import RentQuery, RentListing


class FacebookIngestion(BaseIngestionSource):
    name = "facebook"

    def fetch(self, query: RentQuery) -> List[RentListing]:
        return [
            RentListing(
                title=f"Facebook rental in {query.city}",
                price=query.budget or 500,
                currency="USD",
                location=query.city,
                source=self.name,
                url="https://facebook.com/mock"
            )
        ]
