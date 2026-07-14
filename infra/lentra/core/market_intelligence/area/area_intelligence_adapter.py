from typing import Dict, Any


class AreaIntelligenceAdapter:
    """
    Normalizes area intelligence into
    Market Intelligence area contract.

    Score contract:
        0-10 scale
    """


    def build(
        self,
        listing: Dict[str, Any],
        raw_area: Dict[str, Any]
    ) -> Dict[str, Any]:

        city = (
            listing.get("city")
            or "unknown"
        )


        country = (
            listing.get("country")
            or "Vietnam"
        )


        overall = (
            raw_area.get("overall_score")
            or raw_area.get("area_score")
            or raw_area.get("score")
            or 5.0
        )


        overall = round(
            float(overall),
            2
        )


        if overall >= 8:

            classification = "premium"

            verdict = "GOOD_FOR_EXPATS"


        elif overall >= 6:

            classification = "good"

            verdict = "ACCEPTABLE"


        elif overall >= 4:

            classification = "average"

            verdict = "WEAK_LOCATION"


        else:

            classification = "poor"

            verdict = "BAD_LOCATION"



        breakdown = raw_area.get(
            "breakdown",
            {}
        )


        profile = {

            "internet":
                5.0,

            "safety":
                5.0,

            "noise":
                5.0,

            "infrastructure":
                5.0,

            "expat_density":
                5.0
        }


        return {

            "score":
                overall,

            "overall_score":
                overall,

            "city":
                city,

            "country":
                country,

            "profile":
                profile,

            "breakdown":
                breakdown,

            "classification":
                classification,

            "verdict":
                verdict,

            "version":
                "area_intelligence_v5"

        }
