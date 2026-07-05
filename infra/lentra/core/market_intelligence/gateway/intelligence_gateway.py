import time
from typing import Dict, Any

from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1
from lentra.core.market_intelligence.signals.providers.risk_provider import RiskSignalProvider
from lentra.core.market_intelligence.signals.providers.ranking_provider import RankingProvider
from lentra.core.market_intelligence.signals.providers.coupling_provider import CouplingSignalProvider


class IntelligenceGateway:

    def __init__(self):
        self.signals_engine = SignalsEngineV1()
        self.risk_provider = RiskSignalProvider()
        self.ranking_provider = RankingProvider()
        self.coupling_provider = CouplingSignalProvider()

        self._engine_keys = ["signals", "risk", "ranking", "enrichment"]

    def compute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        start = time.time()

        # 1. signals
        signals = self.signals_engine.build(payload)
        ctx = {**payload, **signals}

        # 2. coupling (SAFE WRAP)
        coupling = self._safe_compute(
            "coupling",
            lambda: self.coupling_provider.compute(ctx)
        )

        ctx2 = {**ctx, "coupling": coupling}

        # 3. risk
        risk = self._safe_compute(
            "risk",
            lambda: self.risk_provider.compute(ctx2)
        )

        ctx3 = {**ctx2, "risk": risk}

        # 4. ranking
        ranking = self._safe_compute(
            "ranking",
            lambda: self.ranking_provider.compute(ctx3)
        )

        duration = time.time() - start

        return {
            "engine_keys": self._engine_keys,
            "pricing": signals.get("pricing"),
            "area": signals.get("area"),
            "dedup": signals.get("dedup"),
            "coupling": coupling,
            "risk": risk,
            "ranking": ranking,
            "meta": {
                "duration_ms": round(duration * 1000, 2)
            }
        }

    def _safe_compute(self, name, fn):
        start = time.time()
        try:
            return fn()
        except Exception as e:
            return {
                "error": str(e),
                "engine": name
            }
        finally:
            dt = (time.time() - start) * 1000
            print(f"[ENGINE:{name}] {dt:.2f}ms")
