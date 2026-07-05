import time
from typing import Dict, Any

from lentra.core.contracts.engine_result import EngineResult


class CouplingSignalProvider:

    name = "coupling"

    def compute(self, ctx: Dict[str, Any]) -> Dict[str, Any]:

        start = time.time()

        pricing = ctx.get("pricing", {})
        area = ctx.get("area", {})

        score = abs(pricing.get("score", 0) - 0.5) * 0.1

        result = {
            "score": score,
            "factors": {
                "price_area_mismatch": pricing.get("score", 0),
                "duplication_pressure": 0.0,
                "market_conflict": 0.0
            }
        }

        return result
