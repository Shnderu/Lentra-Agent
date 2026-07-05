from typing import Dict, Any

from lentra.core.contracts.pipeline_context import PipelineContext
from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1


class IntelligenceGateway:
    """
    Entry point for Market Intelligence OS
    """

    def __init__(self):
        self.signals = SignalsEngineV1()

    def compute(self, data: Dict[str, Any]) -> Dict[str, Any]:

        # STEP 1.1 — freeze entry into immutable context
        ctx = PipelineContext(raw=data)

        # IMPORTANT:
        # engines are still dict-compatible in STEP 1
        signals_result = self.signals.build(data)

        # attach result WITHOUT mutating ctx (still transitional mode)
        result = {
            **signals_result,
            "enrichment": {
                "pricing": signals_result.get("pricing"),
                "area": signals_result.get("area"),
                "dedup": signals_result.get("dedup"),
                "coupling": signals_result.get("coupling"),
                "risk": signals_result.get("risk"),
                "ranking": signals_result.get("ranking"),
                "meta": {
                    "layer": "gateway_v1",
                    "ctx_mode": "immutable_ready"
                }
            }
        }

        # return final API contract unchanged
        return result
