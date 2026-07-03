from typing import Dict, Any
from lentra.core.market_intelligence.signals.signal_contract import Signal, SignalContract


class SignalNormalizer:
    """
    Converts raw engine outputs -> canonical SignalContract
    """

    def normalize(self, engine_outputs: Dict[str, Any]) -> SignalContract:

        pricing_raw = engine_outputs.get("pricing", {})
        risk_raw = engine_outputs.get("risk", {})
        area_raw = engine_outputs.get("area", {})
        dedup_raw = engine_outputs.get("dedup", {})

        return SignalContract(
            pricing=Signal(
                score=float(pricing_raw.get("score", 0.0)),
                confidence=float(pricing_raw.get("confidence", 1.0)),
                source="pricing_engine",
                meta=pricing_raw,
            ),
            risk=Signal(
                score=float(risk_raw.get("risk_level", risk_raw.get("score", 0.0))),
                confidence=float(risk_raw.get("confidence", 1.0)),
                source="risk_engine",
                meta=risk_raw,
            ),
            area=Signal(
                score=float(area_raw.get("score", 0.0)),
                confidence=float(area_raw.get("confidence", 1.0)),
                source="area_engine",
                meta=area_raw,
            ),
            dedup=Signal(
                score=float(dedup_raw.get("score", 0.0)),
                confidence=float(dedup_raw.get("confidence", 1.0)),
                source="dedup_engine",
                meta=dedup_raw,
            ),
        )
