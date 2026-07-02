import time
from typing import Any, Dict


class RuntimeWatchdog:
    """
    ENGINE + SYSTEM LIVENESS SUPERVISOR

    Responsibilities:
    - detect broken engines
    - expose system health
    - provide restart hints (NOT executing restarts)
    """

    def __init__(self, gateway):
        self.gateway = gateway
        self.last_check = time.time()

    def health(self) -> Dict[str, Any]:
        engines = self.gateway.handle({"__probe__": True})

        return {
            "status": "ok",
            "engines_active": list(engines.get("_meta", {}).get("engines", [])),
            "timestamp": time.time(),
            "uptime_check": True
        }

    def check_engines(self) -> Dict[str, Any]:
        try:
            result = self.gateway.handle({"__probe__": True})
            return {"ok": True, "engines": result.get("_meta", {}).get("engines", [])}
        except Exception as e:
            return {"ok": False, "error": str(e)}
