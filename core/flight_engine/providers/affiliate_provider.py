import os
import httpx
from typing import List

from core.flight_engine.gateway.providers.base import BaseProvider
from core.flight_engine.gateway.dto import FlightOffer


class AffiliateProvider(BaseProvider):

    BASE_URL = "https://api.travelpayouts.com/aviasales/v3"

    def __init__(self):
        self.token = os.getenv("TRAVELPAYOUTS_TOKEN")

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        if not self.token:
            print("[AFFILIATE] missing token")
            return []

        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": date,
            "currency": "usd",
            "market": "ru",
            "limit": 10,
            "token": self.token
        }

        try:
            async with httpx.AsyncClient(timeout=15) as client:

                resp = await client.get(
                    f"{self.BASE_URL}/prices_for_dates",
                    params=params
                )

                if resp.status_code != 200:
                    print("[AFFILIATE] bad response", resp.status_code)
                    return []

                data = resp.json()

                offers: List[FlightOffer] = []

                for item in data.get("data", []):

                    offers.append(
                        FlightOffer(
                            origin=origin,
                            destination=destination,
                            date=date,
                            price=item.get("price"),
                            currency="USD",
                            duration="N/A",
                            airline=item.get("airline", "UNKNOWN"),
                            provider="affiliate",
                            raw=item
                        )
                    )

                return offers

        except Exception as e:
            print("[AFFILIATE ERROR]", e)
            return []
