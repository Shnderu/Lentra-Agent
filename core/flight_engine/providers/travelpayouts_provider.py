import os
import httpx
from typing import List

from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.gateway.providers.base import BaseProvider


class TravelpayoutsProvider(BaseProvider):

    BASE_URL = "https://api.travelpayouts.com/aviasales/v3"

    def __init__(self):
        self.token = os.getenv("TRAVELPAYOUTS_TOKEN")
        self.marker = os.getenv("TRAVELPAYOUTS_MARKER", "flyrum")

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        if not self.token:
            print("[TRAVELPAYOUTS] missing token")
            return []

        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": date,
            "currency": "EUR",
            "market": "ru",
            "limit": 10,
            "token": self.token,
            "marker": self.marker
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(
                    f"{self.BASE_URL}/prices_for_dates",
                    params=params
                )

            if response.status_code != 200:
                print("[TRAVELPAYOUTS ERROR]", response.text)
                return []

            data = response.json()

            offers = []

            for item in data.get("data", []):

                offers.append(
                    FlightOffer(
                        origin=origin,
                        destination=destination,
                        date=date,
                        price=item.get("price", 0),
                        currency=item.get("currency", "EUR"),
                        duration="N/A",
                        airline=item.get("airline", "unknown"),
                        provider="travelpayouts",
                        raw=item
                    )
                )

            return offers

        except Exception as e:
            print("[TRAVELPAYOUTS EXCEPTION]", e)
            return []
