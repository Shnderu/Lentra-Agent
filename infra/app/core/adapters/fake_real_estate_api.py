import time
import random
from typing import List
from app.core.contracts.source_contract import BaseRentSource
from app.core.contracts.listing_dto import ListingDTO


class FakeRealEstateAPI(BaseRentSource):
    """
    Имитация реального внешнего API:
    - latency
    - нестабильность
    - вариативный формат
    """

    def search(self, query: str) -> List[ListingDTO]:
        # simulate network latency
        time.sleep(random.uniform(0.15, 0.35))

        # simulate partial failures
        if random.random() < 0.05:
            raise Exception("External API timeout")

        city = "Bangkok" if "bangkok" in query.lower() else "Unknown"

        raw_results = [
            {
                "title": "Luxury Condo Central",
                "price": 900,
                "city": city,
                "url": "https://fake.api/listing/1"
            },
            {
                "title": "Budget Studio Near BTS",
                "price": 400,
                "city": city,
                "url": "https://fake.api/listing/2"
            }
        ]

        return [
            ListingDTO(
                title=i["title"],
                price=i["price"],
                city=i["city"],
                source="real_estate_api",
                url=i["url"]
            )
            for i in raw_results
        ]
