from typing import List
from lentra.bot.features.rent_search.providers.base import RentProvider
from lentra.bot.features.rent_search.contracts import RentSearchItem
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext


class RentAggregator:

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        results: List[RentSearchItem] = []

        for provider in self.providers:
            try:
                results.extend(provider.search(context))
            except Exception:
                # пока fail-safe
                continue

        return results
