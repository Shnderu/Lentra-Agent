from typing import Dict, Any

from lentra.core.market_intelligence.explanation.user_explanation_engine import (
    UserExplanationEngine
)


class ObjectIntelligenceCardBuilder:
    """
    Product contract builder.

    Converts Market Intelligence signals
    into stable Object Intelligence Card.

    v9:
    Adds unified area_intelligence contract
    while preserving legacy area field.
    """

    def __init__(self):

        self.user_explanation = UserExplanationEngine()


    def _extract_dedup(
        self,
        dedup: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(dedup, dict):
            return {}

        nested = dedup.get(
            "dedup",
            {}
        )

        if isinstance(nested, dict):
            return nested

        return dedup


    def _extract_risk(
        self,
        risk: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(risk, dict):
            return {}

        nested = risk.get(
            "risk",
            {}
        )

        if isinstance(nested, dict):
            return nested

        return risk


    def _build_area_intelligence(
        self,
        area: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(area, dict):
            return {}


        return {

            "district":
                area.get(
                    "district"
                ),

            "district_score":
                area.get(
                    "district_score",
                    0
                ),

            "listing_score":
                area.get(
                    "listing_score",
                    0
                ),

            "final_score":
                area.get(
                    "final_area_score",
                    area.get(
                        "overall_score",
                        0
                    )
                ),

            "profile":
                area.get(
                    "profile",
                    {}
                ),

            "district_profile":
                area.get(
                    "district_profile",
                    {}
                ),

            "classification":
                area.get(
                    "classification",
                    "unknown"
                ),

            "verdict":
                area.get(
                    "verdict",
                    "unknown"
                ),

            "version":
                area.get(
                    "version",
                    "unknown"
                )
        }


    def build(
        self,
        listing: Dict[str, Any],
        intelligence: Dict[str, Any],
        ranking: Dict[str, Any],
        decision: Dict[str, Any] = None
    ) -> Dict[str, Any]:

        market = intelligence.get(
            "market",
            {}
        )

        verdict = intelligence.get(
            "market_verdict",
            {}
        )


        segment_signal = intelligence.get(
            "segment_signal",
            {}
        )


        risk = self._extract_risk(
            intelligence.get(
                "risk",
                {}
            )
        )


        dedup = self._extract_dedup(
            intelligence.get(
                "dedup",
                {}
            )
        )


        area = intelligence.get(
            "area",
            {}
        )


        area_intelligence = self._build_area_intelligence(
            area
        )


        decision = decision or {}


        price = listing.get(
            "price",
            0
        )


        market_price = market.get(
            "market_price",
            0
        )


        difference_percent = market.get(
            "difference_percent",
            0
        )


        segment_key = listing.get(
            "segment_key",
            "unknown"
        )


        segment_market = intelligence.get(
            "segment_market",
            {}
        ).get(
            segment_key,
            {}
        )


        if difference_percent < 0:

            market_position = "UNDER_MARKET"

            saving_amount = abs(
                price - market_price
            )

            overpay_amount = 0


        elif difference_percent > 0:

            market_position = "OVER_MARKET"

            saving_amount = 0

            overpay_amount = (
                price - market_price
            )


        else:

            market_position = "FAIR_MARKET"

            saving_amount = 0

            overpay_amount = 0


        duplicates = dedup.get(
            "duplicates",
            0
        )


        risk_level = (
            risk.get(
                "level"
            )
            or
            risk.get(
                "risk_level"
            )
            or
            "unknown"
        )


        recommendation = (
            decision.get(
                "decision"
            )
            or
            "REVIEW"
        )


        return {

            "price": price,

            "market_price": market_price,

            "difference_percent": difference_percent,

            "segment_key":
                segment_key,

            "segment_market":
                {
                    "median_price":
                        segment_market.get(
                            "median_price",
                            0
                        ),

                    "sample_size":
                        segment_market.get(
                            "sample_size",
                            0
                        ),

                    "price_min":
                        segment_market.get(
                            "price_min",
                            0
                        ),

                    "price_max":
                        segment_market.get(
                            "price_max",
                            0
                        )
                },

            "market_position": market_position,

            "saving_amount": saving_amount,

            "overpay_amount": overpay_amount,


            "price_signal":
                (
                    market.get(
                        "price_signal"
                    )
                    or
                    risk.get(
                        "price_signal"
                    )
                    or
                    "unknown"
                ),


            "risk": risk,

            "risk_summary": risk_level,


            "duplicates": duplicates,

            "duplicate_sources":
                dedup.get(
                    "sources",
                    []
                ),


            "market_trend":
                intelligence.get(
                    "price_intelligence",
                    {}
                ).get(
                    "trend",
                    "unknown"
                ),


            "area_intelligence":
                area_intelligence,


            "ai_verdict": verdict,


            "segment_signal":
                segment_signal,


            "decision": decision,



            "explanation":
                self.user_explanation.explain(
                    {
                        "difference_percent":
                            difference_percent,

                        "risk":
                            risk,

                        "duplicates":
                            duplicates,

                        "decision":
                            decision
                    }
                ),


            "ranking": ranking

        }
