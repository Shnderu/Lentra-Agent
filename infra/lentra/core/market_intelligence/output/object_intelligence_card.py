from typing import Dict, Any

from lentra.core.market_intelligence.explanation.user_explanation_engine import (
    UserExplanationEngine
)


class ObjectIntelligenceCardBuilder:

    def __init__(self):
        self.user_explanation = UserExplanationEngine()

    """
    Builds final product intelligence card.

    Converts internal Market Intelligence signals
    into user-facing object intelligence.
    """

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

        risk = intelligence.get(
            "risk",
            {}
        )

        dedup = intelligence.get(
            "dedup",
            {}
        )

        area = intelligence.get(
            "area",
            {}
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

        duplicates = dedup.get(
            "dedup",
            {}
        ).get(
            "duplicates",
            0
        )

        risk_data = risk.get(
            "risk",
            {}
        )

        risk_level = (
            risk_data.get(
                "level"
            )
            or
            risk_data.get(
                "risk_level"
            )
            or
            "unknown"
        )

        if difference_percent < 0:

            market_position = "UNDER_MARKET"

            saving_amount = abs(
                price - market_price
            )

            overpay_amount = 0

        elif difference_percent > 0:

            market_position = "OVER_MARKET"

            overpay_amount = (
                price - market_price
            )

            saving_amount = 0

        else:

            market_position = "FAIR_MARKET"

            saving_amount = 0

            overpay_amount = 0


        recommendation = decision.get(
            "decision",
            "REVIEW"
        )


        return {

            "price":
                price,

            "market_price":
                market_price,

            "difference_percent":
                difference_percent,

            "market_position":
                market_position,

            "saving_amount":
                saving_amount,

            "overpay_amount":
                overpay_amount,

            "price_signal":
                (
                    market.get(
                        "price_signal"
                    )
                    or
                    verdict.get(
                        "signals",
                        {}
                    ).get(
                        "price_signal"
                    )
                    or
                    "unknown"
                ),

            "risk":
                risk_data,

            "risk_summary":
                risk_level,

            "duplicates":
                duplicates,

            "duplicate_sources":
                dedup.get(
                    "dedup",
                    {}
                ).get(
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

            "area":
                area,

            "ai_verdict":
                verdict,

            "decision":
                decision,

            "ai_recommendation":
                recommendation,

            "explanation":
                self.user_explanation.explain(
                    {
                        "price":
                            price,

                        "market_price":
                            market_price,

                        "difference_percent":
                            difference_percent,

                        "risk":
                            risk_data,

                        "duplicates":
                            duplicates,

                        "decision":
                            decision
                    }
                ),

            "ranking":
                ranking
        }
