# ============================================================
# PATCH V17.0 - AGENT MODE
# ============================================================

import time

from lentra.rent.domain_v1 import SearchRentHandler
from lentra.state.storage.memory import MemoryStateStore
from lentra.events.service import EventService
from lentra.cache.services.search_cache import SearchCacheService
from lentra.observability.service import ObservabilityService

from lentra.agent.core.intent import Intent
from lentra.agent.core.agent import RentAgent


class SearchService:
    def __init__(self):
        self.handler = SearchRentHandler()
        self.state = MemoryStateStore()
        self.events = EventService()
        self.cache = SearchCacheService()
        self.obs = ObservabilityService()
        self.agent = RentAgent()

    async def search(self, request: dict):
        start = time.time()

        user_id = request.get("user_id", "anon")

        cached = self.cache.get(request)
        if cached:
            return cached

        session = self.state.get_session(user_id)
        if not session:
            session = self.state.create_session(user_id)

        result = await self.handler.handle({
            "id": "api_request",
            "type": "search_rent",
            "payload": request,
        })

        items = result.get("results", [])

        signals = self.events.get_signals(user_id)

        intent = Intent(
            user_id=user_id,
            goal=request.get("goal", "explore"),
            constraints=request
        )

        agent_result = await self.agent.run(intent, items)

        response = {
            "items": agent_result["result"],
            "steps": agent_result["steps"],
            "user_id": user_id,
            "mode": "v17_agent",
        }

        self.cache.set(request, response)

        return response
