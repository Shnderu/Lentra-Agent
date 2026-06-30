from typing import List, Optional
from lentra.core.market_intelligence.contracts.pipeline_contract import Listing, EnrichedListing


class EngineContract:
    """
    SINGLE SOURCE OF TRUTH CONTRACT FOR AI OS ENGINE
    """

    def analyze(
        self,
        listings: List[Listing],
        query_text: Optional[str] = None
    ) -> List[EnrichedListing]:
        raise NotImplementedError
