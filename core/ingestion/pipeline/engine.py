import asyncio
from core.domain import RentResult
from core.ingestion.transport.rate_limiter import RateLimiter
from core.ingestion.transport.retry import retry
from core.ingestion.pipeline.registry import ProviderRegistry


class IngestionEngine:

    def __init__(self):
        self.registry = ProviderRegistry()

    async def _fetch_provider(self, provider, query):
        limiter = RateLimiter(provider.rate_limit)

        def sync_fetch():
            limiter.acquire()
            return provider.fetch(query)

        return await asyncio.to_thread(
            lambda: retry(sync_fetch)
        )

    async def run(self, query):
        tasks = [
            self._fetch_provider(p, query)
            for p in self.registry.get_all()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        listings = []
        sources = []

        for r, p in zip(results, self.registry.get_all()):
            if isinstance(r, Exception):
                continue
            listings.extend(r)
            sources.append(p.name)

        return RentResult(
            listings=listings,
            sources_used=sources,
            meta={"mode": "async_ingestion_v1"}
        )
