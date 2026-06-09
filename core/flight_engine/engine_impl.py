import asyncio
import hashlib

from core.flight_engine.providers.aviasales import AviasalesProvider
from core.flight_engine.providers.kiwi import KiwiProvider
from core.flight_engine.cache import get_cache, set_cache
from core.flight_engine.normalizer import FlightNormalizer
from core.flight_engine.ranker import FlightRanker


class FlightEngineImpl:

    def __init__(self):
        self.providers = [
            AviasalesProvider(),
            KiwiProvider()
        ]

        self.normalizer = FlightNormalizer()
        self.ranker = FlightRanker()

    def _cache_key(self, origin, destination, date):
        raw = f"{origin}:{destination}:{date}"
        return hashlib.md5(raw.encode()).hexdigest()

    async def search(self, origin: str, destination: str, date: str):

        key = self._cache_key(origin, destination, date)

        cached = get_cache(key)
        if cached:
            print("[CACHE HIT]")
            return cached

        tasks = [p.search(origin, destination, date) for p in self.providers]

        results_raw = await asyncio.gather(*tasks, return_exceptions=True)

        merged = []

        for r in results_raw:
            if isinstance(r, list):
                merged.extend(r)

        normalized = self.normalizer.normalize(merged)

        ranked = self.ranker.rank(normalized)

        set_cache(key, ranked, ttl=300)

        return ranked
