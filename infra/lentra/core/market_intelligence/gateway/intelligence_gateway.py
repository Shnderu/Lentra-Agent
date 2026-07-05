from typing import Dict, Any

from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1
from lentra.core.market_intelligence.signals.providers.risk_provider import RiskSignalProvider
from lentra.core.market_intelligence.signals.providers.ranking_provider import RankingSignalProvider
from lentra.core.market_intelligence.signals.providers.coupling_provider import CouplingSignalProvider

from lentra.core.observability.trace_store import trace_store
from lentra.core.contracts.engine_context import EngineContext


class IntelligenceGateway:

    def __init__(self):
        self.signals_engine = SignalsEngineV1()
        self.risk_provider = RiskSignalProvider()
        self.ranking_provider = RankingSignalProvider()
        self.coupling_provider = CouplingSignalProvider()

        self._engine_keys = ["signals", "coupling", "risk", "ranking"]

    def compute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        request_id = trace_store.new_request_id()
        trace_store.start(request_id)

        ctx = EngineContext(
            payload=payload,
            meta={},
            request_id=request_id
        )

        # 1. signals
        signals = self.signals_engine.build(payload)
        ctx.signals = signals

        # 2. coupling
        coupling = self.coupling_provider.compute({
            **payload,
            **signals
        })
        ctx.meta["coupling"] = coupling

        # 3. risk
        risk = self.risk_provider.compute({
            **payload,
            **signals,
            "coupling": coupling
        })
        ctx.meta["risk"] = risk

        # 4. ranking
        ranking = self.ranking_provider.compute({
            **payload,
            **signals,
            "coupling": coupling,
            "risk": risk
        })

        return {
            "request_id": request_id,
            "engine_keys": self._engine_keys,
            "pricing": signals.get("pricing"),
            "area": signals.get("area"),
            "dedup": signals.get("dedup"),
            "coupling": coupling,
            "risk": risk,
            "ranking": ranking
        }
