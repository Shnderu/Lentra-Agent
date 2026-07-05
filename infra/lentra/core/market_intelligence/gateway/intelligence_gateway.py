from typing import Dict, Any

from lentra.core.market_intelligence.signals.signals_engine_v1 import SignalsEngineV1
from lentra.core.market_intelligence.signals.providers.risk_provider import RiskSignalProvider
from lentra.core.market_intelligence.signals.providers.ranking_provider import RankingSignalProvider
from lentra.core.market_intelligence.signals.providers.coupling_provider import CouplingSignalProvider

from lentra.core.market_intelligence.engine_wrapper import EngineWrapper
from lentra.core.observability.observability_engine_v1 import ObservabilityEngineV1


class IntelligenceGateway:

    def __init__(self):

        self.obs = ObservabilityEngineV1()

        self.signals_engine = SignalsEngineV1()
        self.risk_provider = RiskSignalProvider()
        self.ranking_provider = RankingSignalProvider()
        self.coupling_provider = CouplingSignalProvider()

        # WRAPPED EXECUTION
        self.coupling = EngineWrapper("coupling", self.coupling_provider.compute, self.obs)
        self.risk = EngineWrapper("risk", self.risk_provider.compute, self.obs)
        self.ranking = EngineWrapper("ranking", self.ranking_provider.compute, self.obs)

        self._engine_keys = ["signals", "coupling", "risk", "ranking"]

    def compute(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        signals = self.signals_engine.build(payload)

        ctx = {**payload, "signals": signals}

        coupling = self.coupling(ctx)
        ctx["coupling"] = coupling

        risk = self.risk(ctx)
        ctx["risk"] = risk

        ranking = self.ranking(ctx)

        return {
            "engine_keys": self._engine_keys,
            "pricing": signals.get("pricing"),
            "area": signals.get("area"),
            "dedup": signals.get("dedup"),
            "coupling": coupling,
            "risk": risk,
            "ranking": ranking,
            "trace": self.obs.dump()
        }
