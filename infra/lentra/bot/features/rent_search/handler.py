from lentra.bot.features.base.context import FeatureContext

from lentra.bot.features.rent_search.application.use_cases.query_parser import QueryParser
from lentra.bot.features.rent_search.application.aggregator.rent_aggregator import RentAggregator
from lentra.bot.features.rent_search.application.services.ranking_service import RankingService
from lentra.bot.features.rent_search.application.services.response_builder import ResponseBuilder
from lentra.bot.features.rent_search.providers.sea.sea_provider import ProviderFactory


class RentSearchHandler:
    """
    SINGLE ENTRY POINT for rent_search feature.
    Clean Lentra Agent pipeline.
    """

    def __init__(self):
        self.parser = QueryParser()
        self.providers = ProviderFactory.build()
        self.aggregator = RentAggregator(
            providers=self.providers.providers
        )
        self.ranking = RankingService()
        self.builder = ResponseBuilder()

    async def handle(self, ctx: FeatureContext) -> str:

        # 1. PARSE QUERY
        context = self.parser.parse(ctx.text)

        # 2. AGGREGATE PROVIDERS
        items = await self.aggregator.search(context)

        # 3. RANKING
        ranked = self.ranking.rank(items, context)

        # 4. RESPONSE
        return self.builder.build(context, ranked)
