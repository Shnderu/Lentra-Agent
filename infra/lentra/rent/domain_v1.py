# ============================================================
# RENT DOMAIN V1 - ROUTER CONTRACT FIX
# ============================================================

from typing import Any, Dict


class RentRouter:

    def __init__(self):
        pass

    async def route(self, task: Dict[str, Any]):
        """
        Minimal routing stub (stable contract layer)
        """
        # TODO: replace with real pipeline later
        return {
            "status": "ok",
            "task_type": task.get("type"),
            "payload": task.get("payload"),
        }


def create_rent_router() -> RentRouter:
    """
    Factory required by worker runtime
    """
    return RentRouter()
