from typing import List, Dict
from core.flight_engine.providers.base import BaseProvider
from core.flight_engine.http_client import HttpClient
from core.flight_engine.retry import retry


class AviasalesProvider(BaseProvider):

    def __init__(self):
        self.client = HttpClient()

    async def search(self, origin: str, destination: str, date: str) -> List[Dict]:

        async def _call():
            url = "https://api.aviasales.com/mock/search"

            return await self.client.get(url, params={
                "origin": origin,
                "destination": destination,
                "date": date
            })

        try:
            await retry(_call)

            return [
                {
                    "airline": "AVIASALES PARTNER",
                    "price": 130,
                    "from": origin,
                    "to": destination,
                    "date": date,
                    "duration": "4h 20m",
                    "provider": "aviasales"
                }
            ]

        except Exception as e:
            print("[AVIASALES ERROR]", e)
            return []
