from typing import Dict, Any
from lentra.services.intelligence import intelligence_service
from lentra.services.dedup_engine import dedup_engine
from lentra.services.price_engine import price_engine
from lentra.services.risk_engine import risk_engine


class MarketIntelligenceEngineV2:

    def analyze(self, intent: Dict[str, Any]) -> Dict[str, Any]:

        query = intent.get("query", "")

        # 1. base intelligence signals
        base = intelligence_service.analyze(query, intent)

        # 2. price engine
        price = price_engine.analyze(intent, base)

        # 3. dedup engine
        dedup = dedup_engine.cluster(intent, base)

        # 4. risk engine
        risk = risk_engine.score(intent, base, price)

        # 5. normalized output contract (CRITICAL)
        return {
            "location": base.get("location_hint"),
            "price_band": base.get("price_band"),
            "signals": base.get("signals"),

            "price": price,
            "dedup": dedup,
            "risk": risk,
        }


market_intelligence_engine = MarketIntelligenceEngineV2()
