from typing import Dict, Any

from lentra.core.market_intelligence.expat.expat_score_engine import (
    ExpatScoreEngine,
)


class PipelineAreaAdapter:

    def __init__(self):
        self.engine = ExpatScoreEngine()

    def evaluate(
        self,
        item: Dict[str, Any],
    ) -> Dict[str, Any]:

        result = self.engine.run(item)

        return {
            "area_score": result.get("area_score", 0.0),
            "expat_score": result.get("expat_score", 0.0),
            "location_context": result.get("location", {}),
        }
