import os
import httpx
from typing import List

from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.gateway.providers.base import BaseProvider


class KiwiProvider(BaseProvider):

    def __init__(self):
        self.api_key = os.getenv("KIWI_API_KEY")

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        if not self.api_key:
            return []

        headers = {
            "apikey": self.api_key
        }

        async with httpx.AsyncClient(timeout=10) as client:

            response = await client.get(
                "https://api.tequila.kiwi.com/v2/search",
                headers=headers,
                params={
                    "fly_from": origin,
                    "fly_to": destination,
                    "date_from": date,
                    "date_to": date,
                    "curr": "EUR"
                }
            )

            if response.status_code != 200:
                return []

            data = response.json()

            if not isinstance(data, dict):
                return []

            offers = []

            for item in data.get("data", []):

                offers.append(
                    FlightOffer(
                        origin=origin,
                        destination=destination,
                        date=date,
                        price=item.get("price"),
                        currency="EUR",
                        duration=str(item.get("duration", {}).get("total", "")),
                        airline=(item.get("airlines") or ["unknown"])[0],
                        provider="kiwi",
                        raw=item
                    )
                )

            return offers
