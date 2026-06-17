import time
from typing import List
from app.core.contracts.source_contract import BaseRentSource
from app.core.contracts.listing_dto import ListingDTO


class MockRentAdapter(BaseRentSource):
    """
    Заглушка внешнего источника (имитация API)
    """

    def search(self, query: str) -> List[ListingDTO]:
        time.sleep(0.1)

        return [
            ListingDTO(
                title="Modern Apartment",
                price=600,
                city="Bangkok",
                source="mock_api"
            ),
            ListingDTO(
                title="Studio Flat",
                price=450,
                city="Bangkok",
                source="mock_api"
            )
        ]
