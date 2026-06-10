from core.flight_engine.gateway.flight_gateway import FlightGateway

from core.flight_engine.providers.mock_provider import MockProvider
from core.flight_engine.providers.kiwi_provider import KiwiProvider
from core.flight_engine.providers.amadeus_provider import AmadeusProvider

from core.flight_engine.ranking.engine_v2 import FlightRankingEngineV2


class FlightEngineImpl:

    def __init__(self):

        self.gateway = FlightGateway(
            providers=[
                KiwiProvider(),
                AmadeusProvider(),
                MockProvider()
            ]
        )

        self.ranker = FlightRankingEngineV2()

    async def search(self, origin: str, destination: str, date: str):

        offers = await self.gateway.search(origin, destination, date)

        ranked = await self.ranker.rank(offers)

        return {
            "origin": origin,
            "destination": destination,
            "date": date,
            "offers": ranked
        }
