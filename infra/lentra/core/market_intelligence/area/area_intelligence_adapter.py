from typing import Dict, Any


class AreaIntelligenceAdapter:
    """
    Normalizes area intelligence
    into Market Intelligence contract.
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


        if overall <= 10:

            normalized = round(
                overall / 10,
                2
            )

        else:

            normalized = 0.5



        raw_profile = raw_area.get(
            "profile",
            {}
        )


        profile = {

            "internet":
                raw_profile.get(
                    "internet",
                    5.0
                ),

            "safety":
                raw_profile.get(
                    "safety",
                    5.0
                ),

            "noise":
                raw_profile.get(
                    "noise",
                    5.0
                ),

            "infrastructure":
                raw_profile.get(
                    "infrastructure",
                    5.0
                ),

            "expat_density":
                raw_profile.get(
                    "expat_density",
                    5.0
                )

        }



        if normalized >= 0.75:

            verdict = "GOOD_FOR_EXPATS"

        elif normalized >= 0.55:

            verdict = "ACCEPTABLE"

        else:

            verdict = "WEAK_LOCATION"



        return {

            "score":
                normalized,

            "overall_score":
                overall,

            "city":
                city,

            "country":
                country,

            "profile":
                profile,

            "breakdown":
                raw_area.get(
                    "breakdown",
                    {}
                ),

            "classification":
                raw_area.get(
                    "area_level",
                    "average"
                ),

            "verdict":
                verdict,

            "version":
                "area_intelligence_v6"

        }
