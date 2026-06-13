# ============================================================
# PRODUCT ROUTER V17.2 - SINGLE ENTRY POINT
# ============================================================

from lentra.core.modes import SystemModes
from lentra.api.services.search_service import SearchService
from lentra.agent.core.agent import RentAgent


class ProductRouter:
    def __init__(self):
        self.search_service = SearchService()
        self.agent = RentAgent()

    async def handle(self, request: dict):
        mode = request.get("mode", SystemModes.SEARCH)

        # -------------------------
        # SEARCH MODE
        # -------------------------
        if mode == SystemModes.SEARCH:
            return await self.search_service.search(request)

        # -------------------------
        # AGENT MODE
        # -------------------------
        if mode == SystemModes.AGENT:
            intent = request.get("intent")
            data = request.get("data", [])
            return await self.agent.run(intent, data)

        # -------------------------
        # AUTONOMOUS MODE
        # -------------------------
        if mode == SystemModes.AUTONOMOUS:
            return await self.agent.start_autonomous_mode(request)

        # -------------------------
        # MONITOR MODE
        # -------------------------
        if mode == SystemModes.MONITOR:
            return {
                "status": "monitoring_mode_placeholder",
                "data": request
            }

        raise Exception(f"Unknown system mode: {mode}")
