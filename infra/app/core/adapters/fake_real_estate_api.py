import time
import random
from typing import List
from app.core.contracts.source_contract import BaseRentSource
from app.core.contracts.listing_dto import ListingDTO


class FakeRealEstateAPI(BaseRentSource):

    def search(self, query: str) -> List[ListingDTO]:
        latency = random.uniform(0.15, 0.5)
        time.sleep(latency)

        # simulate degradation
        if random.random() < 0.15:
            raise TimeoutError("API timeout")

        city = "Bangkok" if "bangkok" in query.lower() else "Unknown"

        return [
            ListingDTO(
                title="Luxury Condo Central",
                price=900,
                city=city,
                source="real_estate_api",
                url="https://fake.api/listing/1"
            ),
            ListingDTO(
                title="Budget Studio Near BTS",
                price=400,
                city=city,
                source="real_estate_api",
                url="https://fake.api/listing/2"
            )
        ]
