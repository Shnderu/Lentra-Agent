from typing import Any, Dict, List


class IntelligenceOrchestrator:
    """
    Центральный слой AI-обогащения объектов рынка.

    ВАЖНО:
    - НЕ делает routing
    - НЕ делает ingestion
    - НЕ заменяет pipeline

    Только:
    enrichment + scoring + annotations
    """

    def __init__(
        self,
        price_engine=None,
        risk_engine=None,
        area_engine=None,
        market_engine=None,
    ):
        self.price_engine = price_engine
        self.risk_engine = risk_engine
        self.area_engine = area_engine
        self.market_engine = market_engine

    def enrich(self, objects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        enriched = []

        for obj in objects:
            enriched_obj = dict(obj)

            # PRICE INTELLIGENCE
            if self.price_engine:
                enriched_obj["price_analysis"] = self.price_engine.evaluate(obj)

            # RISK SCORING
            if self.risk_engine:
                enriched_obj["risk"] = self.risk_engine.score(obj)
            else:
                enriched_obj["risk"] = {"level": "unknown", "score": 0.5}

            # AREA INTELLIGENCE
            if self.area_engine:
                enriched_obj["area"] = self.area_engine.score(obj)

            # MARKET CONTEXT
            if self.market_engine:
                enriched_obj["market"] = self.market_engine.compare(obj)

            # DERIVED FIELDS (fallback logic)
            enriched_obj["ai_flags"] = self._derive_flags(enriched_obj)

            enriched.append(enriched_obj)

        return enriched

    def _derive_flags(self, obj: Dict[str, Any]) -> Dict[str, Any]:
        flags = {
            "is_overpriced": False,
            "is_suspicious": False,
            "is_good_deal": False,
        }

        price = obj.get("price_analysis", {})
        risk = obj.get("risk", {})

        if isinstance(price, dict):
            if price.get("deviation", 0) > 0.1:
                flags["is_overpriced"] = True

            if price.get("deviation", 0) < -0.1:
                flags["is_good_deal"] = True

        if isinstance(risk, dict):
            if risk.get("score", 0) > 0.7:
                flags["is_suspicious"] = True

        return flags
