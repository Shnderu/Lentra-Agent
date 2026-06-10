from typing import List

from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.gateway.providers.base import BaseProvider


class AmadeusProvider(BaseProvider):

    def __init__(self):
        self.api_key = None  # пока заглушка

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:
        # fallback stub
        return []
