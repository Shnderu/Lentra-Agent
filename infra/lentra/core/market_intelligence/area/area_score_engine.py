
from lentra.core.market_intelligence.models.market_object import MarketObject


class AreaScoreEngine:

    def run(self, obj: MarketObject) -> MarketObject:

        # defaults
        area = {
            "area_score": 5.0,
            "internet": 5.0,
            "noise": 5.0,
            "expat_density": 5.0,
        }

        # signal 1: listings geo hints
        for l in obj.listings:

            text = (l.location + " " + l.title).lower()

            # beach areas
            if "beach" in text or "my khe" in text:
                area["area_score"] += 1.5
                area["expat_density"] += 1.0
                area["internet"] += 0.5

            # inland downgrade
            if "inland" in text:
                area["area_score"] -= 1.0
                area["noise"] += 0.5

            # luxury signal
            if "luxury" in text or "sea view" in text:
                area["area_score"] += 1.0
                area["noise"] -= 0.5

        # clamp values
        for k in area:

            area[k] = max(0.0, min(10.0, area[k]))

        obj.area_score = area["area_score"]
        obj.area_profile = area

        return obj
