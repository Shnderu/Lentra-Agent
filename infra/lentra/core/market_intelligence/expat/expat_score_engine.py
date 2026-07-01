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

        result = {
            "expat_score": min(score, 1.0),
            "location": location
        }

        return result

    def evaluate(self, payload: dict):
        """
        Unified Gateway contract.
        """

        result = self.score(payload)

        return {
            "area_score": result.get("expat_score", 0.0),
            **result,
        }
