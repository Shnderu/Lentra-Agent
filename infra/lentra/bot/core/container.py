from lentra.rent.repository import RentRepository
from lentra.telegram.bot_factory import build_bot

class Container:
    def __init__(self):
        # rent layer
        self.rent_repository = RentRepository()

        # telegram bot (ВАЖНО: возвращаем как DI объект)
        self.bot = build_bot()

        # временные заглушки
        self.scoring = None
        self.filters = None
        self.connectors = None


def build_container():
    return Container()
