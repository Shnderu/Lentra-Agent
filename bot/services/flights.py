from bot.events.bus import publish
from bot.events.types import FLIGHT_PRICE_EVENT


def ingest_flight_price(data: dict):
    """
    data example:
    {
        "route": "MOW-AMS",
        "price": 120,
        "target_price": 150
    }
    """

    publish(FLIGHT_PRICE_EVENT, data)
