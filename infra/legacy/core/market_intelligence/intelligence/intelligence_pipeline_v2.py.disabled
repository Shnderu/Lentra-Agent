from lentra.core.market_intelligence.areas.area_engine_v2 import AreaEngineV2
from lentra.core.market_intelligence.deduplication.dedup_engine_v2 import DedupEngineV2


class IntelligencePipelineV2:

    def __init__(self):

        self.area = AreaEngineV2()
        self.dedup = DedupEngineV2()

    def process(self, listings):

        # 1. AREA NORMALIZATION
        listings = [self.area.process(l) for l in listings]

        # 2. DEDUPLICATION
        listings = self.dedup.process(listings)

        return listings
