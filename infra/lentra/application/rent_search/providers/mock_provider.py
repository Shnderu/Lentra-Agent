from typing import List
from lentra.application.rent_search.providers.base import RentProvider
from lentra.application.rent_search.contracts import RentSearchItem
from lentra.application.rent_search.dto.search_context import SearchContext


class MockProvider(RentProvider):

    def search(self, context: SearchContext) -> List[RentSearchItem]:

        return [
            RentSearchItem(
                title="Modern apartment near center",
                price="1200$",
                city=context.city or "unknown"
            ),
            RentSearchItem(
                title="Cheap studio",
                price="600$",
                city=context.city or "unknown"
            ),
        ]
