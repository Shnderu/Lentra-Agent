from typing import List
from core.sources.base import BaseSource
from core.domain import RentQuery, RentListing


class FaswazSource(BaseSource):
    name = "faswaz"

    def search(self, query: RentQuery) -> List[RentListing]:
        return [
            RentListing(
                title="Faswaz Apartment in " + query.city,
                price=(query.budget or 700) - 100,
                currency="USD",
                location=query.city,
                source=self.name,
                url="https://faswaz.com/mock"
            )
        ]
