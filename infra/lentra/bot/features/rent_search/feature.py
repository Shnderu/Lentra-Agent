from lentra.bot.features.rent_search.service import RentSearchService


class RentSearchFeature:
    """
    Единая точка входа в rent_search feature.
    Handler не знает про service напрямую.
    """

    def __init__(self, service: RentSearchService):
        self.service = service

    async def search(self, request):
        return await self.service.search(request)
