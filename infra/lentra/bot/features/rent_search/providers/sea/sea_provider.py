from typing import List
import asyncio

from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem

from lentra.bot.features.rent_search.providers.sea.thailand_provider import ThailandProvider
from lentra.bot.features.rent_search.providers.social.social_provider import SocialProvider
from lentra.bot.features.rent_search.providers.scraper.scraper_provider import ScraperProvider


class SEAProvider(RentProvider):

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


class ProviderFactory:

    @staticmethod
    def build():

        return SEAProvider(
            providers=[
                ThailandProvider(),
                SocialProvider(),
                ScraperProvider()
            ]
        )
