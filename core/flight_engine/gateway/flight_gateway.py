from typing import List

from core.flight_engine.gateway.dto import FlightOffer


class FlightGateway:

    def __init__(self, providers):
        self.providers = providers

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        all_offers: List[FlightOffer] = []

        for provider in self.providers:

            try:
                offers = await provider.search(origin, destination, date)

                if offers:
                    all_offers.extend(offers)

            except Exception as e:
                print(f"[GATEWAY ERROR] {provider.__class__.__name__}: {e}")

        return all_offers
