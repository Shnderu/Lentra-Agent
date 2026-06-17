from dataclasses import dataclass

from lentra.bot.features.rent_search.service import RentSearchService
from lentra.rent.connectors.default_connector import DefaultConnector


@dataclass
class Container:
    rent_search_service: RentSearchService
    bot: object = None


def build_container():
    connector = DefaultConnector()

    rent_service = RentSearchService(
        connectors=[connector]
    )

    container = Container(
        rent_search_service=rent_service,
        bot=None
    )

    print("[BOOT] CONTAINER BUILT")

    return container
