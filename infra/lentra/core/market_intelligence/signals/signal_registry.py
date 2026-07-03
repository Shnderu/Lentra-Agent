from typing import Dict, Any, List

from lentra.core.market_intelligence.signals.providers.pricing_provider import PricingSignalProvider
from lentra.core.market_intelligence.signals.providers.risk_provider import RiskSignalProvider
from lentra.core.market_intelligence.signals.providers.area_provider import AreaSignalProvider
from lentra.core.market_intelligence.signals.providers.dedup_provider import DedupSignalProvider


class SignalRegistry:
    """
    Single authority for all MI signals.
    """

    def __init__(self):
        self.providers = [
            PricingSignalProvider(),
            RiskSignalProvider(),
            AreaSignalProvider(),
            DedupSignalProvider(),
        ]

    def build(self, engine_outputs: Dict[str, Any]) -> Dict[str, Any]:
        result = {}

        for p in self.providers:
            result[p.name] = p.compute(engine_outputs)

        return result
