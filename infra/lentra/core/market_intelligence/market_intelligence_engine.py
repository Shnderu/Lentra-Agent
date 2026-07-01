from typing import Dict, Any

from lentra.core.market_intelligence.output.facade_guarded import MarketIntelligenceOutputFacadeGuarded
from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.market_intelligence.pricing.pricing_adapter import PricingAdapter

from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
from lentra.core.market_intelligence.risk.risk_engine import RiskEngine
from lentra.core.market_intelligence.expat.expat_engine_v2 import ExpatEngineV2

from lentra.core.market_intelligence.decision.local_verdict_resolver import resolve_verdict
from lentra.core.market_intelligence.signals.signal_normalizer import SignalNormalizer
from lentra.core.market_intelligence.governance.governance_lock import GovernanceLock


class MarketIntelligenceEngine:

    def __init__(self):

        self.output_facade = MarketIntelligenceOutputFacadeGuarded()

        self.pricing_engine = PricingAdapter(PricingEngine())
        self.risk_engine = RiskEngine()
        self.expat_engine = ExpatEngineV2()

        self.dedup_engine = UnifiedDedupEngine()

    def analyze(self, payload: Dict[str, Any]):
        context = self._run_core_graph(payload)
        return self.output_facade.analyze(context)

    def _run_core_graph(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        price = payload.get("price", 0)

        price_raw = self.pricing_engine.get_market_price(payload)
        market_price = price_raw.get("market_price", 0)

        deviation = ((price - market_price) / market_price * 100) if market_price else 0.0

        dedup = self.dedup_engine.deduplicate([payload])

        risk = self.risk_engine.evaluate(payload)
        risk = self.risk_engine.apply_dedup_signal(risk, dedup)

        expat_raw = self.expat_engine.process(payload)
        signals = SignalNormalizer.normalize(expat_raw)

        verdict = resolve_verdict(
            deviation=deviation,
            risk_level=risk.get("risk_level", "unknown")
        )

        base_meta = {
            "trace_id": "flatten-v3",
            "confidence": 0.80,
            "regime": {"regime": "stable"}
        }

        governance = GovernanceLock.stabilize(base_meta)

        return {
            "ui": {
                "price": price,
                "market_price": market_price,
                "deviation_pct": deviation,
                "risk_level": risk.get("risk_level", "unknown"),
                "duplicates": dedup.get("duplicates", 0),
                "verdict": verdict
            },
            "api": {
                "normalized": {"price": price},
                "signals": signals,
                "scores": {},
            },
            "meta": {
                **base_meta,
                "governance": governance
            }
        }
