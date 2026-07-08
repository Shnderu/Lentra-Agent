# ============================================================
# SEARCH SERVICE V18.0 - MARKET INTELLIGENCE ENTRYPOINT
# ============================================================

import time

from lentra.core.market_intelligence.engines.dedup_engine import DedupEngine
from lentra.core.market_intelligence.engines.risk_engine import RiskEngine
from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.engines.area_engine import AreaEngine

from lentra.core.adapters.search_adapter import SearchAdapter
from lentra.core.pipeline.canonical_search_pipeline import CanonicalSearchPipeline

from lentra.agent.core.intent import Intent
from lentra.agent.core.agent import RentAgent

from lentra.state.storage.memory import MemoryStateStore
from lentra.cache.services.search_cache import SearchCacheService
from lentra.events.service import EventService
from lentra.observability.service import ObservabilityService


class IntelligenceSearchEngine:

    def __init__(self):
        self.adapter = SearchAdapter()

        self.dedup_engine = DedupEngine()
        self.risk_engine = RiskEngine()
        self.market_engine = PricingEngine()
        self.area_engine = AreaEngine()

        self.pipeline = CanonicalSearchPipeline(
            self
        )

    def fetch(self, query):
        return self.adapter.build_objects(query)

    def normalize(self, listings):
        return listings

    def dedup(self, listings):
        return [
            self.dedup_engine.run(
                item
            )
            for item in listings
        ]

    def rank(self, listings):
        return sorted(
            listings,
            key=lambda x: x.get(
                "relevance_score",
                0
            ),
            reverse=True
        )

    def risk(self, listings):
        result = []

        for item in listings:
            risk = self.risk_engine.run(
                item
            )

            item["risk"] = risk

            result.append(item)

        return result

    def run(self, query):
        return self.pipeline.run(query)


class SearchService:

    def __init__(self):

        self.engine = IntelligenceSearchEngine()

        self.state = MemoryStateStore()
        self.events = EventService()
        self.cache = SearchCacheService()
        self.obs = ObservabilityService()

        self.agent = RentAgent()


    async def search(self, request: dict):

        start = time.time()

        user_id = request.get(
            "user_id",
            "anon"
        )

        cached = self.cache.get(
            request
        )

        if cached:
            return cached


        query = request.get(
            "query",
            ""
        )


        items = self.engine.run(
            query
        )


        intent = Intent(
            user_id=user_id,
            goal=request.get(
                "goal",
                "explore"
            ),
            constraints=request
        )


        agent_result = await self.agent.run(
            intent,
            items
        )


        response = {
            "items": agent_result.get(
                "result",
                items
            ),
            "steps": agent_result.get(
                "steps",
                []
            ),
            "user_id": user_id,
            "mode": "v18_market_intelligence",
            "processing_time": round(
                time.time() - start,
                4
            )
        }


        self.cache.set(
            request,
            response
        )


        return response
