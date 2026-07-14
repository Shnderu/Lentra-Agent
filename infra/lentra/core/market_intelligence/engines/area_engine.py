from typing import Dict, Any

from lentra.core.engines.base_engine import BaseEngine

from lentra.core.market_intelligence.area.area_intelligence import (
    compute_area_intelligence
)

from lentra.core.market_intelligence.area.area_intelligence_adapter import (
    AreaIntelligenceAdapter
)


class AreaEngine(BaseEngine):
    """
    Canonical Market Intelligence Area Engine.

    Production bridge:

    context
        |
        v
    feature normalization
        |
        v
    area_intelligence heuristic model
        |
        v
    AreaIntelligenceAdapter
        |
        v
    normalized area intelligence contract
    """

    def __init__(self):

        self.adapter = AreaIntelligenceAdapter()


    def _extract_features(
        self,
        ctx: Dict[str, Any]
    ):

        features = []

        existing = ctx.get(
            "features",
            []
        )

        if isinstance(existing, list):
            features.extend(existing)


        text = " ".join(
            [
                str(ctx.get("title", "")),
                str(ctx.get("description", "")),
                str(ctx.get("query", "")),
            ]
        ).lower()


        if "internet" in text or "wifi" in text:
            features.append("internet")


        if "studio" in text:
            features.append("studio")


        if "central" in text or "center" in text:
            features.append("central")


        if "beach" in text or "my khe" in text or "sea" in text:
            features.append("beach")


        return list(
            set(features)
        )


    def run(
        self,
        ctx: Dict[str, Any]
    ) -> Dict[str, Any]:

        city = (
            ctx.get("city")
            or "unknown"
        )


        listing = {

            "city": city,

            "country":
                ctx.get(
                    "country",
                    "Vietnam"
                ),

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
                self._extract_features(
                    ctx
                ),

        }


        raw_area = compute_area_intelligence(
            listing,
            {
                "listings_count": 5
            }
        )


        return self.adapter.build(
            listing,
            raw_area
        )
