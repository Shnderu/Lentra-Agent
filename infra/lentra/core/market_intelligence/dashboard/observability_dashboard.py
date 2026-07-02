from typing import Dict, Any
import time


class ObservabilityDashboard:
    """
    LIGHTWEIGHT PRODUCTION OBSERVABILITY LAYER

    Responsibilities:
    - collect engine execution stats
    - expose runtime snapshot
    - no business logic modifications
    """

    def __init__(self):
        self.metrics = {
            "requests": 0,
            "latency_ms": [],
            "errors": 0,
            "last_updated": None
        }

    def record_request(self, latency_ms: float, error: bool = False):
        self.metrics["requests"] += 1
        self.metrics["latency_ms"].append(latency_ms)

        if error:
            self.metrics["errors"] += 1

        self.metrics["last_updated"] = time.time()

    def snapshot(self) -> Dict[str, Any]:
        lat = self.metrics["latency_ms"]

        return {
            "requests": self.metrics["requests"],
            "errors": self.metrics["errors"],
            "avg_latency_ms": sum(lat) / len(lat) if lat else 0,
            "engines_active": True,
            "status": "ok",
            "last_updated": self.metrics["last_updated"]
        }
