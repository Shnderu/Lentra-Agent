from core.flight_engine.mock_provider import MockProvider


class FlightEngineImpl:
    def __init__(self):
        self.providers = [
            MockProvider()
        ]

    async def search(self, origin: str, destination: str, date: str):

        results = []

        for provider in self.providers:
            data = await provider.search(origin, destination, date)
            results.extend(data)

        # сортировка по цене
        results.sort(key=lambda x: x.get("price", 999999))

        return results
