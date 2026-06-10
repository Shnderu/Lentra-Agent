import os
from typing import List

from core.flight_engine.gateway.adapters.base import BaseAdapter
from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.http_client import HttpClient


class KiwiAdapter(BaseAdapter):

    BASE_URL = "https://api.tequila.kiwi.com/v2"

    def __init__(self):
        self.api_key = os.getenv("KIWI_API_KEY")
        self.http = HttpClient()

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        if not self.api_key:
            print("[KIWI] missing API key")
            return []

        headers = {
            "apikey": self.api_key
        }

        params = {
            "fly_from": origin,
            "fly_to": destination,
            "date_from": date,
            "date_to": date,
            "curr": "USD",
            "limit": 5
        }

        try:
            data = await self.http.get(
                f"{self.BASE_URL}/search",
                headers=headers,
                params=params
            )

            offers = []

            for item in data.get("data", []):

                offers.append(
                    FlightOffer(
                        origin=origin,
                        destination=destination,
                        date=date,
                        price=item.get("price", 9999),
                        currency="USD",
                        duration=f"{item.get('duration', {}).get('total', 0)//60}m",
                        airline="KIWI",
                        provider="kiwi",
                        raw=item
                    )
                )

            return offers

        except Exception as e:
            print("[KIWI ERROR]", e)
            return []
