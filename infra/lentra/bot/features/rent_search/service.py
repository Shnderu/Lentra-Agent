from lentra.bot.features.rent_search.repository import RentRepository
from lentra.bot.features.rent_search.mapper import map_to_cards
from lentra.bot.features.rent_search.application.use_cases.query_parser import QueryParser
from lentra.bot.features.rent_search.application.services.ranking_service import RankingService
from lentra.bot.features.rent_search.application.services.response_builder import ResponseBuilder


class RentSearchService:
    def __init__(self, repository: RentRepository):
        self.repository = repository
        self.parser = QueryParser()
        self.ranker = RankingService()
        self.builder = ResponseBuilder()

    def search(self, query: str):

        context = self.parser.parse(query)

        raw = self.repository.search(context.query)

        items = map_to_cards(raw)

        ranked = self.ranker.rank(items, context)

        response_text = self.builder.build(context, ranked)

        return response_text
