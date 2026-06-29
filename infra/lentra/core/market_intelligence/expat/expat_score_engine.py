class ExpatScoreEngine:
    """
    Safe expat scoring engine (robust to legacy string location format)
    """

    def score(self, listing: dict):

        location = listing.get("location", {})

        # FIX: normalize string → dict
        if isinstance(location, str):
            location = {
                "segment": location,
                "micro_market": location
            }

        segment = location.get("segment", "")
        micro = location.get("micro_market", "")

        # simple scoring v1
        score = 0.5

        if "beach" in segment:
            score += 0.2

        if "premium" in segment:
            score += 0.2

        return {
            "expat_score": min(score, 1.0),
            "location": location
        }
