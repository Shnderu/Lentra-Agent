from lentra.core.market_intelligence.intelligence.intelligence_pipeline_v2 import IntelligencePipelineV2
from lentra.core.market_intelligence.contracts.engine_registry import EngineRegistry

from lentra.core.market_intelligence.risk.risk_engine_v2 import RiskEngineV2
from lentra.core.market_intelligence.expat.expat_engine_v2 import ExpatEngineV2
from lentra.core.market_intelligence.comparison.comparison_engine_v2 import ComparisonEngineV2


class MarketIntelligenceEngine:

    def __init__(self):

        # ARCHAELOGY LAYER (MANDATORY PREPROCESS)
        self.intel = IntelligencePipelineV2()

        # ENGINE LAYER (DETERMINISTIC CHAIN)
        self.registry = EngineRegistry()

        # register canonical engines only
        self.registry.register(RiskEngineV2())
        self.registry.register(ExpatEngineV2())
        self.registry.register(ComparisonEngineV2())

    def analyze(self, listings, query_text=None):

        # =========================
        # STEP 1: INTELLIGENCE LAYER (MANDATORY)
        # =========================
        listings = self.intel.process(listings)

        # =========================
        # STEP 2: ENGINE REGISTRY (MANDATORY)
        # =========================
        listings = self.registry.run_all(listings)

        return listings
