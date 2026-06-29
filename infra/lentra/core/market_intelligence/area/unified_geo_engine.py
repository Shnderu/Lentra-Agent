from lentra.core.market_intelligence.area.area_engine import AreaEngine
from lentra.core.market_intelligence.area.market_segmentation_engine import MarketSegmentationEngine
from lentra.core.market_intelligence.area.micro_market_engine import MicroMarketEngine
from lentra.core.market_intelligence.area.temporal_market_engine import TemporalMarketEngine


class UnifiedGeoEngine:
    """
    SINGLE GEO PIPELINE
    """

    def __init__(self):
        self.area = AreaEngine()
        self.segmenter = MarketSegmentationEngine()
        self.micro = MicroMarketEngine()
        self.temporal = TemporalMarketEngine()

    def process(self, listing: dict):
        listing = self.area.evaluate(listing)

        listing["segment"] = self.segmenter.update(listing)
        listing["micro_market"] = self.micro.update(listing)
        listing["temporal_signal"] = self.temporal.volatility(listing["micro_market"])

        return listing
