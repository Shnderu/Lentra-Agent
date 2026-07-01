from typing import Dict, Any

from lentra.core.market_intelligence.output import MarketIntelligenceOutputFacadeGuarded
from lentra.core.market.pricing_engine import PricingEngine
from lentra.core.market_intelligence.dedup.unified_dedup_engine import UnifiedDedupEngine
from lentra.core.market_intelligence.risk.risk_engine import RiskEngine
from lentra.core.market_intelligence.expat.expat_engine_v2 import ExpatEngineV2

from lentra.core.market_intelligence.decision.signal_authority_resolver import SignalAuthorityResolver
from lentra.core.market_intelligence.signals.signal_normalizer import SignalNormalizer
from lentra.core.market_intelligence.conflict.conflict_engine import ConflictEngine
from lentra.core.market_intelligence.governor.weight_governor import WeightGovernor
from lentra.core.market_intelligence.fusion.signal_fusion_engine import SignalFusionEngine

from lentra.core.market_intelligence.memory.signal_memory import SignalMemory
from lentra.core.market_intelligence.learning.signal_learner import SignalLearner
from lentra.core.market_intelligence.learning.decision_feedback import DecisionFeedbackEngine
from lentra.core.market_intelligence.regime.market_regime_engine import MarketRegimeEngine

from lentra.core.market_intelligence.governor.signal_authority_governor_v2 import SignalAuthorityGovernorV2
from lentra.core.market_intelligence.policy.signal_policy_kernel import SignalPolicyKernel

from lentra.core.market_intelligence.governance.governance_constitution import GovernanceConstitution


class MarketIntelligenceEngine:

    def __init__(self):
        self.output_facade = MarketIntelligenceOutputFacadeGuarded()

        self.pricing_engine = PricingEngine()
        self.dedup_engine = UnifiedDedupEngine()
        self.risk_engine = RiskEngine()
        self.expat_engine = ExpatEngineV2()

        self.authority = SignalAuthorityResolver()
        self.normalizer = SignalNormalizer()
        self.conflict = ConflictEngine()
        self.governor = WeightGovernor()
        self.fusion = SignalFusionEngine()

        self.memory = SignalMemory()
        self.learner = SignalLearner()

        self.regime_engine = MarketRegimeEngine()
        self.feedback_engine = DecisionFeedbackEngine()

        self.meta_governor = SignalAuthorityGovernorV2()
        self.policy_kernel = SignalPolicyKernel()

        # FINAL LAYER
        self.constitution = GovernanceConstitution()

    def analyze(self, payload: Dict[str, Any]):
        context = self._run_core_graph(payload)
        return self.output_facade.analyze(context)

    def _get_market_price(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        if hasattr(self.pricing_engine, "analyze"):
            return self.pricing_engine.analyze(payload)
        return {"market_price": payload.get("price", 0)}

    def _run_core_graph(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        price = payload.get("price", 0)

        price_raw = self._get_market_price(payload)
        market_price = price_raw.get("market_price", 0)

        deviation = ((price - market_price) / market_price * 100) if market_price else 0.0

        dedup = self.dedup_engine.analyze(payload)
        risk = self.risk_engine.evaluate(payload)
        expat = self.expat_engine.process(payload)

        ui = {
            "price": price,
            "market_price": market_price,
            "deviation_pct": deviation,
            "risk_level": risk.get("risk_level", "unknown"),
            "duplicates": dedup.get("duplicates", 0),
        }

        api = {
            "normalized": {"price": price},
            "signals": {
                "area_score": expat.get("score", 0),
                "internet_score": expat.get("internet", 0),
                "noise_score": expat.get("noise", 0),
            },
            "scores": {},
        }

        meta = {
            "trace_id": "stable-core-v11",
            "confidence": 0.72,
        }

        resolved = self.authority.resolve(ui, api, meta)

        ui["risk_level"] = resolved.final_risk_level
        meta["authority_trace"] = resolved.authority_trace

        signals = self.normalizer.normalize(ui, api)

        self.memory.add(signals)

        drift = self.memory.detect_drift(signals)
        learning = self.learner.learn(self.memory.get_history())
        regime = self.regime_engine.detect(self.memory.get_history())
        feedback = self.feedback_engine.evaluate(self.memory.get_history())

        meta["learning"] = learning
        meta["drift"] = drift
        meta["regime"] = regime
        meta["feedback"] = feedback

        meta_policy = self.policy_kernel.apply(meta)
        meta["policy"] = meta_policy

        # -------------------------
        # FINAL GOVERNANCE LAYER
        # -------------------------
        governance = self.constitution.resolve(meta)
        meta["governance"] = governance

        meta["confidence"] = governance["confidence"]

        conflict_result = self.conflict.resolve(signals)

        governed_signals = self.governor.adjust(
            signals,
            conflict_result["conflicts"]
        )

        fused = self.fusion.fuse(ui, api, meta)

        fused["signals"] = governed_signals
        fused["conflicts"] = conflict_result["conflicts"]
        fused["adjustments"] = conflict_result["adjustments"]

        return fused
