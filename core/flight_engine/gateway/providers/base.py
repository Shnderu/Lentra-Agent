from abc import ABC, abstractmethod
from typing import List
from core.flight_engine.gateway.dto import FlightOffer


class BaseProvider(ABC):

    @abstractmethod
    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:
        pass
