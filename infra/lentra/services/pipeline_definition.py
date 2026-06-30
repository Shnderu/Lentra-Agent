from lentra.core.market_intelligence.market_intelligence_engine import MarketIntelligenceEngine


class PipelineDefinition:

    def __init__(self):
        self.intel = MarketIntelligenceEngine()

    def run(self, property_object):
        """
        SINGLE SOURCE OF TRUTH PIPELINE
        """
        return self.intel.analyze([property_object])
