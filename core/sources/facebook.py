from typing import List
from core.sources.base import BaseSource
from core.domain import RentQuery, RentListing


class FacebookSource(BaseSource):
    name = "facebook"

    def search(self, query: RentQuery) -> List[RentListing]:
        return [
            RentListing(
                title="FB Rental in " + query.city,
                price=query.budget or 500,
                currency="USD",
                location=query.city,
                source=self.name,
                url="https://facebook.com/mock"
            )
        ]
