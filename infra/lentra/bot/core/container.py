from lentra.bot.features.rent_search.data.mock_provider import MockRentDataProvider
from lentra.bot.features.rent_search.repository import RentRepository


class Container:
    """
    DI root (минимальный стабильный вариант)
    """

    def __init__(self):
        provider = MockRentDataProvider()
        self.rent_repository = RentRepository(provider=provider)
