import asyncio


class ProviderManager:

    def __init__(self, adapters):
        self.adapters = adapters

    async def collect(self, origin: str, destination: str, date: str):

        tasks = [
            a.search(origin, destination, date)
            for a in self.adapters
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        merged = []

        for r in results:
            if isinstance(r, Exception):
                print("[ADAPTER ERROR]", r)
                continue
            merged.extend(r)

        return merged
