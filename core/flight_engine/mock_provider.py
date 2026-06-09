from typing import List, Dict


class MockProvider:
    async def search(self, origin: str, destination: str, date: str) -> List[Dict]:

        return [
            {
                "airline": "FLYRUM TEST",
                "price": 120,
                "from": origin,
                "to": destination,
                "date": date,
                "duration": "4h 10m"
            },
            {
                "airline": "DEMO AIR",
                "price": 140,
                "from": origin,
                "to": destination,
                "date": date,
                "duration": "4h 25m"
            }
        ]
