from lentra.core.pipeline.context import PipelineContext
from typing import Dict, Any


class SignalsEngineV2:
    """
    Immutable signals engine (V2)
    """

    def compute(self, ctx: PipelineContext) -> PipelineContext:

        data = ctx.raw

        pricing = self._pricing_signal(data)
        area = self._area_signal(data)
        dedup = self._dedup_signal(data)

        return ctx.with_update(
            pricing=pricing,
            area=area,
            dedup=dedup
        )

    def _pricing_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = data.get("price", 0)
        market = data.get("market_price", 0)

        if not market:
            return {"score": 0.0, "deviation": 0.0}

        deviation = (price - market) / market

        return {
            "score": min(abs(deviation), 1.0),
            "direction": "over" if deviation > 0 else "under",
            "deviation": round(deviation, 4),
        }

    def _area_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": 0.5, "note": "enhanced_area_model"}

    def _dedup_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {"score": 1.0, "confidence": 1.0}
