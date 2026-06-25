from typing import List
import asyncio

from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem

from lentra.rent.connectors.scraper_connector import ScraperConnector


class ScraperProvider(RentProvider):

    def __init__(self):
        self.connector = ScraperConnector()

    async def search(self, context: SearchContext) -> List[RentSearchItem]:

        # blocking IO → thread-safe wrapper
        raw = await asyncio.to_thread(
            self.connector.fetch,
            {
                "city": context.city,
                "text": context.query
            }
        )

        items = []

        for r in raw:
            items.append(
                RentSearchItem(
                    title=r.get("title"),
                    price=str(r.get("price")),
                    city=r.get("city"),
                    source=r.get("source", "scraper")
                )
            )

        return items
