from lentra.core.market_intelligence.dedup.dedup_v2 import DedupV2Engine
from lentra.core.market_intelligence.duplicate.duplicate_engine import DuplicateEngine


class UnifiedDedupEngine:
    """
    SINGLE ENTRY POINT for all dedup logic.
    Safe wrapper over legacy systems.
    """

    def __init__(self):
        self.v2 = DedupV2Engine()
        self.legacy = DuplicateEngine()

    def process(self, listings: list):
        # Step 1: modern dedup
        listings = self.v2.process(listings)

        # Step 2: legacy compatibility cleanup
        listings = self.legacy.clean(listings)

        return listings
