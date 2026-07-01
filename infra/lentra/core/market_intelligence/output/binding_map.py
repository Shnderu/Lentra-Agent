from typing import Dict, Any


class IntelligenceBindingMap:
    """
    Центральная карта проекции intelligence layers → output contract.
    Без бизнес-логики. Только маршрутизация данных.
    """

    @staticmethod
    def map(engine_result: Dict[str, Any]) -> Dict[str, Any]:

        return {
            # -------------------------
            # PRICE / MARKET
            # -------------------------
            "ui.price": engine_result.get("price"),
            "ui.market_price": engine_result.get("market_price"),
            "ui.deviation_pct": engine_result.get("deviation_pct"),

            # -------------------------
            # RISK
            # -------------------------
            "ui.risk_level": engine_result.get("risk_level"),
            "meta.confidence": engine_result.get("confidence"),

            # -------------------------
            # DEDUP
            # -------------------------
            "ui.duplicates": engine_result.get("duplicates"),

            # -------------------------
            # EXPLANATION
            # -------------------------
            "ui.explanation": engine_result.get("explanation"),
            "ui.verdict": engine_result.get("verdict"),

            # -------------------------
            # AREA / EXPAT INTELLIGENCE
            # -------------------------
            "ui.area": engine_result.get("area"),

            # -------------------------
            # MARKET DYNAMICS
            # -------------------------
            "api.dynamics": engine_result.get("dynamics"),

            # -------------------------
            # SIGNALS / SCORES
            # -------------------------
            "api.signals": engine_result.get("signals"),
            "api.scores": engine_result.get("scores"),

            # -------------------------
            # META EXTENSION
            # -------------------------
            "meta.confidence_breakdown": engine_result.get("confidence_breakdown"),
            "meta.source_count": engine_result.get("source_count"),
            "meta.trace_id": engine_result.get("trace_id", "unknown"),
        }
