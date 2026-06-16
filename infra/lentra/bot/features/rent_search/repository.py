from lentra.bot.features.rent_search.data.provider import RentDataProvider


class RentRepository:
    """
    Оркестратор data layer.
    """

    def __init__(self, provider: RentDataProvider):
        self.provider = provider

    def search(self, query: str):
        return self.provider.fetch(query)
