from lentra.bot.features.rent_search.repository import RentRepository
from lentra.bot.features.rent_search.mapper import map_to_cards
from lentra.bot.features.rent_search.application.use_cases.query_parser import RentQueryParser
from lentra.bot.features.rent_search.application.services.ranking_service import RentRankingService
from lentra.bot.features.rent_search.application.services.response_builder import RentResponseBuilder
from lentra.bot.features.rent_search.models import RentalSearchResult


class RentSearchService:
    def __init__(self):
        self.repo = RentRepository()
        self.parser = RentQueryParser()
        self.ranker = RentRankingService()
        self.builder = RentResponseBuilder()

    def search(self, req):

        parsed = self.parser.parse(req.query)

        raw = self.repo.fetch_listings(
            query=parsed.raw_text,
            city=parsed.city,
        )

        cards = map_to_cards(raw)
        ranked = self.ranker.rank(cards)

        message = self.builder.build(ranked)

        return RentalSearchResult(cards=ranked, message=message)
