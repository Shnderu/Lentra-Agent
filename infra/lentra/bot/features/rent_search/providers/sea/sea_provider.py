from typing import List
from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem
from lentra.bot.features.rent_search.application.services.normalizer import RentNormalizer


class SEAProvider(RentProvider):

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers
        self.normalizer = RentNormalizer()

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        results: List[RentSearchItem] = []

        for provider in self.providers:
            try:
                items = provider.search(context)

                for item in items:
                    normalized = self.normalizer.normalize(
                        item,
                        country=getattr(context, "country", None)
                    )
                    results.append(normalized)

            except Exception:
                continue

        return results
