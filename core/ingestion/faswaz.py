from typing import List
from core.ingestion.base import BaseIngestionSource
from core.domain import RentQuery, RentListing


class FaswazIngestion(BaseIngestionSource):
    name = "faswaz"

    def fetch(self, query: RentQuery) -> List[RentListing]:
        return [
            RentListing(
                title=f"Faswaz rental in {query.city}",
                price=(query.budget or 700) - 120,
                currency="USD",
                location=query.city,
                source=self.name,
                url="https://faswaz.com/mock"
            )
        ]
