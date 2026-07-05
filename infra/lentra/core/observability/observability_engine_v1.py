import time
from typing import Dict, Any, List


class ObservabilityEngineV1:
    """
    Collects execution telemetry for all engines
    """

    def __init__(self):
        self.timings: List[Dict[str, Any]] = []

    def trace(self, engine_name: str, fn, *args, **kwargs):
        start = time.time()

        result = fn(*args, **kwargs)

        end = time.time()

        self.timings.append({
            "engine": engine_name,
            "duration_ms": round((end - start) * 1000, 4)
        })

        return result

    def dump(self) -> Dict[str, Any]:
        total = sum(t["duration_ms"] for t in self.timings)

        return {
            "total_ms": round(total, 4),
            "engines": self.timings
        }
