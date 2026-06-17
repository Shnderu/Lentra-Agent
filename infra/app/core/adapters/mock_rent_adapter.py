import time
from typing import List
from app.core.contracts.source_contract import BaseRentSource
from app.core.contracts.listing_dto import ListingDTO


class MockRentAdapter(BaseRentSource):
    def search(self, query: str) -> List[ListingDTO]:
        time.sleep(0.08)

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
            ),
            ListingDTO(  # дубль для проверки dedup
                title="Studio Flat",
                price=450,
                city="Bangkok",
                source="mock_api"
            )
        ]
