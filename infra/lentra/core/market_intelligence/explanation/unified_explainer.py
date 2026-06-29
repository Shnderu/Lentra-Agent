from lentra.core.market_intelligence.explanation.decision_narrative_engine import DecisionNarrativeEngine


class UnifiedExplainer:
    """
    SINGLE explanation layer.
    """

    def __init__(self):
        self.engine = DecisionNarrativeEngine()

    def explain(self, listing: dict):
        return self.engine.explain(listing)
