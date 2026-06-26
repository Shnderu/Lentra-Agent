class RiskScorer:
    """
    NO CROSS MODULE FEEDBACK
    """

    def score(self, listing: dict):
        return {
            "risk_score": 0.5,
            "flags": []
        }
