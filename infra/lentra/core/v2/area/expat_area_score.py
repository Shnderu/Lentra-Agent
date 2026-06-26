from typing import Dict, Any


class ExpatAreaScoreV2:

    def score(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        v2 area intelligence layer (SEA / Vietnam MVP)
        """

        location = (listing.get("location") or "").lower()

        # MVP heuristic model (позже заменим на geo + dataset)
        base = 7.0

        # near beach bonus
        if "beach" in location:
            base += 1.2

        # central / city penalty
        if "center" in location or "downtown" in location:
            base -= 0.5

        # default city adjustment (Da Nang baseline)
        if "da nang" in location:
            base += 0.3

        # noise / infrastructure placeholders (future data layer)
        internet = 8.5
        noise = 5.5
        expats = 7.8

        return {
            "area_score": round(base, 2),
            "internet": internet,
            "noise": noise,
            "expats": expats
        }
