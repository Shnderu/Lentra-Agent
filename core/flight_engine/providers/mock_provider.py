from typing import List

from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.gateway.providers.base import BaseProvider


class MockProvider(BaseProvider):

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        return [
            FlightOffer(
                origin=origin,
                destination=destination,
                date=date,
                price=100,
                currency="EUR",
                duration="2h 30m",
                airline="MOCK",
                provider="mock",
                raw={}
            )
        ]
