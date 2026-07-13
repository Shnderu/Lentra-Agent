from typing import List
from lentra.application.rent_search.providers.base.provider import RentProvider
from lentra.application.rent_search.dto.search_context import SearchContext
from lentra.application.rent_search.contracts.rent_item import RentSearchItem


class SocialProvider(RentProvider):

    country = None  # глобальный источник (пока)

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        # пока stub, позже Telegram/FB scraping
        return []
