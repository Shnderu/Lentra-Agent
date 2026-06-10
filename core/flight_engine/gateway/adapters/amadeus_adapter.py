import os
from typing import List

from core.flight_engine.gateway.adapters.base import BaseAdapter
from core.flight_engine.gateway.dto import FlightOffer
from core.flight_engine.http_client import HttpClient


class AmadeusAdapter(BaseAdapter):

    BASE_URL = "https://test.api.amadeus.com"

    def __init__(self):
        self.client_id = os.getenv("AMADEUS_CLIENT_ID")
        self.client_secret = os.getenv("AMADEUS_CLIENT_SECRET")
        self.token = None
        self.http = HttpClient()

    async def _auth(self):

        if not self.client_id or not self.client_secret:
            print("[AMADEUS] missing credentials")
            return

        data = await self.http.post(
            f"{self.BASE_URL}/v1/security/oauth2/token",
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }
        )

        self.token = data.get("access_token")

    async def search(self, origin: str, destination: str, date: str) -> List[FlightOffer]:

        if not self.token:
            await self._auth()

        if not self.token:
            return []

        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        params = {
            "originLocationCode": origin,
            "destinationLocationCode": destination,
            "departureDate": date,
            "adults": 1,
            "currencyCode": "USD",
            "max": 5
        }

        try:
            data = await self.http.get(
                f"{self.BASE_URL}/v2/shopping/flight-offers",
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
                        price=float(item.get("price", {}).get("total", 9999)),
                        currency="USD",
                        duration=item.get("itineraries", [{}])[0].get("duration", ""),
                        airline=(item.get("validatingAirlineCodes") or ["AMADEUS"])[0],
                        provider="amadeus",
                        raw=item
                    )
                )

            return offers

        except Exception as e:
            print("[AMADEUS ERROR]", e)
            return []
