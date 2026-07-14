from typing import Dict, Any

from lentra.core.engines.base_engine import BaseEngine

from lentra.core.market_intelligence.area.area_intelligence import (
    compute_area_intelligence
)

from lentra.core.market_intelligence.area.area_intelligence_adapter import (
    AreaIntelligenceAdapter
)

from lentra.core.market_intelligence.area.district_intelligence import (
    detect_district,
    get_district_intelligence
)



class AreaEngine(BaseEngine):
    """
    Canonical Market Intelligence Area Engine v7.

    Pipeline:

    listing context
          |
          v
    Listing Area Intelligence
          |
          +
          |
          v
    District Intelligence
          |
          v
    Unified Area Contract
    """



    def __init__(self):

        self.adapter = AreaIntelligenceAdapter()



    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:


        city = (
            ctx.get("city")
            or "unknown"
        )


        country = (
            ctx.get("country")
            or "Vietnam"
        )


        listing = {

            "city": city,

            "country": country,

            "location":
                ctx.get(
                    "location",
                    ""
                ),

            "title":
                ctx.get(
                    "title",
                    ""
                ),

            "description":
                ctx.get(
                    "description",
                    ""
                ),

            "features":
                ctx.get(
                    "features",
                    []
                )
        }



        # Listing level intelligence

        raw_area = compute_area_intelligence(
            listing,
            {
                "listings_count": 5
            }
        )



        # District level intelligence

        district = detect_district(
            listing
        )


        district_intelligence = get_district_intelligence(
            district
        )



        listing_score = raw_area.get(
            "area_score",
            5.0
        )


        district_score = district_intelligence.get(
            "score",
            5.0
        )



        # weighted final score
        # 60% object signals
        # 40% district context

        final_score = round(
            (
                listing_score * 0.6
            )
            +
            (
                district_score * 0.4
            ),
            2
        )



        raw_area["district"] = district

        raw_area["district_score"] = district_score

        raw_area["listing_score"] = listing_score

        raw_area["final_area_score"] = final_score

        raw_area["district_profile"] = (
            district_intelligence.get(
                "profile",
                {}
            )
        )



        result = self.adapter.build(
            listing,
            raw_area
        )


        result["district"] = district

        result["district_score"] = district_score

        result["listing_score"] = listing_score

        result["final_area_score"] = final_score

        result["district_profile"] = (
            district_intelligence.get(
                "profile",
                {}
            )
        )


        result["version"] = "area_intelligence_v7"


        return result
