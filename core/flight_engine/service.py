from core.flight_engine.engine_impl import FlightEngineImpl


class FlightSearchService:

    def __init__(self):
        self.engine = FlightEngineImpl()

    async def search(self, origin: str, destination: str, date: str):

        if not origin or not destination or not date:
            raise ValueError("Missing required parameters")

        return await self.engine.search(origin, destination, date)
