class Ranker:
    """
    FINAL SCORING LAYER ONLY

    INPUT ONLY FROM PIPELINE CONTEXT
    """

    def rank(self, listings: list):
        return sorted(listings, key=lambda x: x.get("price", 0))
