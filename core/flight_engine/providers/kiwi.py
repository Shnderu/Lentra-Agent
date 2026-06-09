from typing import List, Dict
from core.flight_engine.providers.base import BaseProvider
from core.flight_engine.http_client import HttpClient
from core.flight_engine.retry import retry


class KiwiProvider(BaseProvider):

    def __init__(self):
        self.client = HttpClient()

    async def search(self, origin: str, destination: str, date: str) -> List[Dict]:

        async def _call():
            # MOCK API ENDPOINT (replace later with real Kiwi API)
            url = "https://api.kiwi.com/mock/search"

            return await self.client.get(url, params={
                "fly_from": origin,
                "fly_to": destination,
                "date": date
            })

        try:
            data = await retry(_call)

            return [
                {
                    "airline": "KIWI AIR",
                    "price": 155,
                    "from": origin,
                    "to": destination,
                    "date": date,
                    "duration": "4h 05m",
                    "provider": "kiwi"
                }
            ]

        except Exception as e:
            print("[KIWI ERROR]", e)
            return []
