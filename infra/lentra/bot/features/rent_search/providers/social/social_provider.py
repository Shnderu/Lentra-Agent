from typing import List
from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem


class SocialProvider(RentProvider):

    country = None  # глобальный источник (пока)

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        # пока stub, позже Telegram/FB scraping
        return []
