from core.product.providers.mock import MockFlightProvider


class FlightService:
    def __init__(self):
        self.provider = MockFlightProvider()

    def search(self, payload: dict):
        origin = payload.get("origin")
        destination = payload.get("destination")

        if not origin or not destination:
            raise ValueError("origin/destination required")

        result = self.provider.search(origin, destination)

        return result.to_dict()
