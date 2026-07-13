from typing import List
import asyncio

from lentra.application.rent_search.providers.base.provider import RentProvider
from lentra.application.rent_search.contracts import RentSearchItem
from lentra.application.rent_search.dto.search_context import SearchContext

from lentra.application.rent_search.providers.sea.thailand_provider import ThailandProvider
from lentra.application.rent_search.providers.sea.vietnam_provider import VietnamProvider
from lentra.application.rent_search.providers.social.social_provider import SocialProvider
from lentra.application.rent_search.providers.scraper.scraper_provider import ScraperProvider


class SEAProvider(RentProvider):

    def __init__(self, providers: List[RentProvider]):
        self.providers = providers

    async def search(self, context: SearchContext) -> List[RentSearchItem]:

        tasks = []

        for provider in self.providers:

            if hasattr(provider, "country"):
                if provider.country and provider.country != context.country:
                    continue

            tasks.append(provider.search(context))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        items: List[RentSearchItem] = []

        for r in results:
            if isinstance(r, Exception):
                continue
            items.extend(r)

        return items


class ProviderFactory:

    @staticmethod
    def build():

        return SEAProvider(
            providers=[
                ThailandProvider(),
                VietnamProvider(),
                SocialProvider(),
                ScraperProvider()
            ]
        )
