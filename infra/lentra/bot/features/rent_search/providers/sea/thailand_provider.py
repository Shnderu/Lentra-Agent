from typing import List
from lentra.bot.features.rent_search.providers.base.provider import RentProvider
from lentra.bot.features.rent_search.application.dto.search_context import SearchContext
from lentra.bot.features.rent_search.contracts.rent_item import RentSearchItem


class ThailandProvider(RentProvider):

    country = "thailand"

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        if context.country != "thailand":
            return []

        return [
            RentSearchItem(
                title="Condo near BTS Asok",
                price="18000 THB",
                city="Bangkok",
                source="mock_th"
            ),
            RentSearchItem(
                title="Studio Chiang Mai Old Town",
                price="9000 THB",
                city="Chiang Mai",
                source="mock_th"
            )
        ]
