from typing import List
from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts import RentSearchItem


class SocialProvider(RentProvider):

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        # позже сюда: FB groups / Telegram scraping

        return []
