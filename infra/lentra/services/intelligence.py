from typing import Dict, Any
from lentra.services.market_intelligence_v2 import MarketIntelligenceV2


class MarketIntelligence(MarketIntelligenceV2):
    """
    Compatibility wrapper:
    старые сценарии ожидают MarketIntelligence
    новая система = MarketIntelligenceV2
    """
    pass


intelligence_service = MarketIntelligence()
