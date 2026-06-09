from typing import List, Dict


class FlightEngine:
    async def search(self, origin: str, destination: str, date: str) -> List[Dict]:
        raise NotImplementedError
