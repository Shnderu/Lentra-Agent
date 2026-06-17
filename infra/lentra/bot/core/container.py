from lentra.rent.repository import RentRepository
from lentra.rent.connectors import *
from lentra.rent.quality.scoring import *
from lentra.rent.quality.filters import *

class Container:
    def __init__(self):
        # ✔ возвращаем контракт, который ожидает handler
        self.rent_repository = RentRepository()

        # остальное временно упрощаем
        self.scoring = None
        self.filters = None
        self.connectors = None


def build_container():
    return Container()
