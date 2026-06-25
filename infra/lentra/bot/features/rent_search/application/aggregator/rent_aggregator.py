from typing import List
import asyncio

from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class RentAggregator:

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers

    async def search(self, context: SearchContext) -> List[RentSearchItem]:

        tasks = [
            provider.search(context)
            for provider in self.providers
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        items: List[RentSearchItem] = []

        for r in results:
            if isinstance(r, Exception):
                continue
            items.extend(r)

        return items
