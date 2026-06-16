from lentra.bot.features.rent_search.mapper import map_to_cards
from lentra.bot.features.rent_search.contract.request import RentalSearchRequest
from lentra.bot.features.rent_search.contract.response import RentalSearchResult


class RentSearchService:
    def __init__(self, repository):
        self.repository = repository

    async def search(self, request: RentalSearchRequest) -> RentalSearchResult:
        raw_results = await self.repository.search(
            query=request.query,
            city=request.city,
            min_price=request.min_price,
            max_price=request.max_price,
        )

        cards = map_to_cards(raw_results)

        return RentalSearchResult(cards=cards)
