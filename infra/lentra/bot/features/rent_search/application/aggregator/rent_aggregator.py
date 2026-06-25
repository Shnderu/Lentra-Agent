from typing import List
import asyncio

from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.services.normalizer import RentNormalizer


class RentAggregator:

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers
        self.normalizer = RentNormalizer()

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

        # -------------------------
        # NORMALIZATION STEP (NEW)
        # -------------------------
        normalized = []
        for item in items:
            try:
                normalized.append(
                    self.normalizer.normalize(
                        item,
                        country=context.country
                    )
                )
            except Exception:
                normalized.append(item)

        return normalized
