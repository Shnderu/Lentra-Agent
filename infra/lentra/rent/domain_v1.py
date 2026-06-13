# ============================================================
# LENTRA RENT DOMAIN LAYER V1 (V15.3 EXTENSION)
# ============================================================

from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol, List
import asyncio
import logging

logger = logging.getLogger("lentra.rent")


# ============================================================
# 1. TASK TYPES (DOMAIN INTENTS)
# ============================================================

class RentTaskType:
    SEARCH_RENT = "search_rent"
    GET_LISTING = "get_listing"
    NOTIFY_NEW_LISTING = "notify_new_listing"


# ============================================================
# 2. CONTRACT SCHEMA (V15.2 EXTENSION)
# ============================================================

RENT_PAYLOAD_SCHEMA = {
    "city": str,
    "budget_min": (int, float, type(None)),
    "budget_max": (int, float, type(None)),
    "rooms": (int, type(None)),
    "area": (str, type(None)),
    "move_in_date": (str, type(None)),
    "source": (str, type(None)),
}


def validate_rent_payload(payload: Dict[str, Any]) -> bool:
    for key, expected in RENT_PAYLOAD_SCHEMA.items():
        if key in payload and not isinstance(payload[key], expected):
            raise ValueError(f"[RENT_CONTRACT] Invalid field: {key}")
    return True


# ============================================================
# 3. INTEGRATION PORT (EXTERNAL SOURCES ABSTRACTION)
# ============================================================

class RentSourceAdapter(Protocol):
    async def search_listings(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        ...


# ============================================================
# 4. DEFAULT ADAPTER (SAFE PLACEHOLDER FOR REAL INTEGRATIONS)
# ============================================================

class DefaultRentAdapter:
    """
    Это НЕ бизнес-логика.
    Это заглушка-интерфейс для будущих:
    - Airbnb adapter
    - Local boards scraper
    - Expat housing APIs
    """

    async def search_listings(self, query: Dict[str, Any]) -> List[Dict[str, Any]]:
        logger.info(f"[ADAPTER] search_listings called with {query}")

        await asyncio.sleep(0.3)

        return [
            {
                "id": "mock_1",
                "title": "Modern studio in center",
                "city": query.get("city"),
                "price": 450,
                "rooms": 1,
                "source": "mock_adapter",
            }
        ]


# ============================================================
# 5. HANDLERS (PURE DOMAIN LOGIC)
# ============================================================

class SearchRentHandler:
    def __init__(self, adapter: RentSourceAdapter):
        self.adapter = adapter

    async def handle(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = task.get("payload", {})

        validate_rent_payload(payload)

        results = await self.adapter.search_listings(payload)

        return {
            "task_id": task["id"],
            "status": "success",
            "results": results,
        }


class ListingDetailHandler:
    async def handle(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = task.get("payload", {})

        listing_id = payload.get("listing_id")
        if not listing_id:
            raise ValueError("[LISTING] listing_id required")

        return {
            "task_id": task["id"],
            "listing_id": listing_id,
            "status": "success",
            "data": {
                "id": listing_id,
                "title": "Stub listing detail",
            },
        }


class NotifyRentHandler:
    async def handle(self, task: Dict[str, Any]) -> Dict[str, Any]:
        payload = task.get("payload", {})

        logger.info(f"[NOTIFY] Rent alert triggered: {payload}")

        return {
            "task_id": task["id"],
            "status": "sent",
        }


# ============================================================
# 6. ROUTER (V15.3 EXTENSION ONLY)
# ============================================================

class RentRouter:
    def __init__(self, adapter: RentSourceAdapter):
        self.handlers = {
            RentTaskType.SEARCH_RENT: SearchRentHandler(adapter),
            RentTaskType.GET_LISTING: ListingDetailHandler(),
            RentTaskType.NOTIFY_NEW_LISTING: NotifyRentHandler(),
        }

    async def route(self, task: Dict[str, Any]) -> Dict[str, Any]:
        task_type = task.get("type")

        handler = self.handlers.get(task_type)
        if not handler:
            raise ValueError(f"[ROUTER] Unknown task type: {task_type}")

        return await handler.handle(task)


# ============================================================
# 7. FACTORY
# ============================================================

def create_rent_router() -> RentRouter:
    adapter = DefaultRentAdapter()
    return RentRouter(adapter)
