from typing import Dict, Any

from lentra.core.market_intelligence.output import MarketIntelligenceOutputFacadeGuarded
from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
# LEGACY REMOVED - unified dedup only
from lentra.core.market_intelligence.risk.risk_engine import RiskEngine
from lentra.core.market_intelligence.expat.expat_score_engine import ExpatScoreEngine
from lentra.core.market_intelligence.decision.local_verdict_resolver import resolve_verdict
from lentra.core.market_intelligence.signals.signal_normalizer import SignalNormalizer
from lentra.core.market_intelligence.governance.governance_lock import GovernanceLock


class MarketIntelligenceEngine:
    """
    STEP 9 FLATTEN CORE ENGINE
    - no multi-decision layers
    - single signal vector
    - deterministic scoring spine
    """

    def __init__(self):

        self.output_facade = MarketIntelligenceOutputFacadeGuarded()

        self.pricing_engine = PricingEngine()
        self.risk_engine = RiskEngine()
        self.expat_engine = ExpatScoreEngine()

        self.unified_dedup_engine = UnifiedDedupEngine()
        self.dedup_engine = self.unified_dedup_engine

    def analyze(self, payload: Dict[str, Any]):
        context = self._run_core_graph(payload)
        return self.output_facade.analyze(context)

    def _build_signal_vector(self, payload: Dict[str, Any], price: float, market_price: float, dedup: dict, risk: dict, expat: dict):
        deviation = ((price - market_price) / market_price * 100) if market_price else 0.0

        signals = SignalNormalizer.normalize(expat)

        return {
            "price": price,
            "market_price": market_price,
            "deviation": deviation,
            "risk_signal": risk,
            "area_signal": signals.get("area_score", 0.0),
            "noise_signal": signals.get("noise_score", 0.0),
            "duplicate_signal": dedup.get("duplicates", 0),
            "expat_signal": signals
        }

    def _score_spine(self, vector: Dict[str, Any]) -> Dict[str, Any]:

        deviation = vector["deviation"]
        risk_level = vector["risk_signal"].get("risk_level", "unknown")

        verdict = resolve_verdict(
            deviation=deviation,
            risk_level=risk_level
        )

        confidence = 0.8 - (abs(deviation) * 0.001)

        return {
            "verdict": verdict,
            "confidence": max(0.1, min(0.95, confidence)),
            "risk_level": risk_level
        }


    def _build_market_stats(self, payload):
        return {
            'market_price': payload.get('price', 0),
            'volatility': 0.0,
            'trend': 'stable'
        }
    def _run_core_graph(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        price = payload.get("price", 0)

        price_raw = self.pricing_engine.score(payload, self._build_market_stats(payload))
        market_price = price_raw.get("market_price", 0)

        dedup = self.dedup_engine.analyze(payload)
        risk = self.risk_engine.evaluate(payload)
        expat_raw = self.expat_engine.score(payload)

        vector = self._build_signal_vector(
            payload,
            price,
            market_price,
            dedup,
            risk,
            expat_raw
        )

        spine = self._score_spine(vector)

        base_meta = {
            "trace_id": "flatten-v4",
            "confidence": spine["confidence"],
            "regime": {"regime": "stable"}
        }

        governance = GovernanceLock.stabilize(base_meta)

        return {
            "ui": {
                "price": price,
                "market_price": market_price,
                "deviation_pct": vector["deviation"],
                "risk_level": spine["risk_level"],
                "duplicates": vector["duplicate_signal"],
                "verdict": spine["verdict"]
            },
            "api": {
                "vector": vector,
                "spine": spine
            },
            "meta": {
                **base_meta,
                "governance": governance
            }
        }

# FLATTEN SHIM (auto-generated)
def _get_market_price(self, payload):
    if hasattr(self.pricing_engine, "get_market_price"):
        return self.pricing_engine.score(payload, self._build_market_stats(payload))
    if hasattr(self.pricing_engine, "score"):
        return self.pricing_engine.score(payload, self._build_market_stats(payload))
    return payload.get("price", 0)


def _build_pricing_engine(self):
    # flattened pricing engine (direct binding)
    return self.pricing_engine


    def _build_market_stats(self, payload):
        # flattened minimal stats contract
        return {
            "market_price": payload.get("price", 0),
            "volatility": 0.0,
            "trend": "stable"
        }
