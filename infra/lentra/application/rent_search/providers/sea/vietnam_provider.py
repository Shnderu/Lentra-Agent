from typing import List
import asyncio

from lentra.application.rent_search.providers.base.provider import RentProvider
from lentra.application.rent_search.dto.search_context import SearchContext
from lentra.application.rent_search.contracts.rent_item import RentSearchItem

from lentra.rent.connectors.scraper_connector import ScraperConnector


class VietnamProvider(RentProvider):

    country = "vietnam"

    def __init__(self):
        self.connector = ScraperConnector()

    async def search(self, context: SearchContext) -> List[RentSearchItem]:

        if context.country != "vietnam":
            return []

        raw = await asyncio.to_thread(
            self.connector.fetch,
            {
                "country": "vietnam",
                "city": context.city,
                "text": context.query
            }
        )

        items: List[RentSearchItem] = []

        for r in raw:

            items.append(
                RentSearchItem(
                    title=r.get("title"),
                    price=str(r.get("price")),
                    city=r.get("city"),
                    source=r.get("source", "vn_scraper"),
                    url=r.get("url")
                )
            )

        return items
