"""
STEP 6 FIX:
Decision layer is deprecated.

All decision logic is now handled by:
MarketIntelligenceEngine.analyze()
"""

class MarketDecisionCore:
    def __init__(self):
        raise RuntimeError(
            "MarketDecisionCore is deprecated. Use MarketIntelligenceEngine instead."
        )
