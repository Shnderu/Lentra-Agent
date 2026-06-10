from typing import List
from core.flight_engine.gateway.dto import FlightOffer


class FlightNormalizer:

    def normalize(self, offers: List[FlightOffer]) -> List[FlightOffer]:
        return offers
