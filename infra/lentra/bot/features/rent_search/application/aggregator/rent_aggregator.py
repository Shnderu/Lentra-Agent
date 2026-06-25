from typing import List
import asyncio

from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext

from lentra.bot.features.rent_search.application.services.normalizer import RentNormalizer
from lentra.bot.features.rent_search.application.services.deduplicator import RentDeduplicator


class RentAggregator:

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers
        self.normalizer = RentNormalizer()
        self.deduplicator = RentDeduplicator()

    async def search(
        self,
        context: SearchContext
    ) -> List[RentSearchItem]:

        tasks = [
            provider.search(context)
            for provider in self.providers
        ]

        results = await asyncio.gather(
            *tasks,
            return_exceptions=True
        )

        items: List[RentSearchItem] = []

        for result in results:

            if isinstance(result, Exception):
                continue

            for item in result:

                normalized = self.normalizer.normalize(
                    item=item,
                    country=context.country
                )

                items.append(normalized)

        items = self.deduplicator.deduplicate(items)

        return items
