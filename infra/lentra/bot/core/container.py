from lentra.bot.features.rent_search.repository import RentRepository
from lentra.bot.features.rent_search.service import RentSearchService


class Container:
    def __init__(self):
        # repositories
        self.rent_repository = RentRepository()

        # services
        self.rent_search_service = RentSearchService(
            repository=self.rent_repository
        )
