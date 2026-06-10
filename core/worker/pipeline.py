import hashlib

from core.intent.llm_classifier import LLMIntentClassifier
from core.flight_engine.service import FlightSearchService
from core.flight_engine.engine_impl import FlightEngineImpl
from core.cache.redis_cache import RedisCache


class WorkerPipeline:

    def __init__(self):
        self.intent = LLMIntentClassifier()
        self.flight = FlightEngineImpl()
        self.cache = RedisCache()

    def _cache_key(self, payload: dict):
        raw = f"{payload['origin']}-{payload['destination']}-{payload['date']}"
        return hashlib.md5(raw.encode()).hexdigest()

    async def run(self, task: dict):

        payload = task["payload"]

        key = self._cache_key(payload)

        # 1. cache check
        cached = await self.cache.get(key)
        if cached:
            return cached

        # 2. intent (optional hook for future routing)
        intent = await self.intent.classify(str(payload))

        # 3. flight search
        result = await self.flight.search(
            payload["origin"],
            payload["destination"],
            payload["date"]
        )

        # 4. cache result
        await self.cache.set(key, result)

        return result
