class AreaEngine:

    def score(self, location: str) -> dict:

        location = (location or "").lower()

        score = 5.0

        if "beach" in location:
            score += 2.0

        if "center" in location or "downtown" in location:
            score += 1.0

        if "wifi" in location:
            score += 0.5

        return {
            "area_quality": min(score, 10.0)
        }
