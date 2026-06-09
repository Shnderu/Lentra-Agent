import random
from core.product.dto.flight import FlightResult


class MockFlightProvider:
    def search(self, origin: str, destination: str):
        price = random.randint(12000, 60000)

        return FlightResult(
            origin=origin,
            destination=destination,
            price=price,
            airline="FlyRum Demo Air"
        )
