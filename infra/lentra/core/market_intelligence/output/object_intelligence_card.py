from typing import Dict, Any


class ObjectIntelligenceCardBuilder:
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

        explanation = intelligence.get(
            "market_explanation",
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

        return {

            "price":
                listing.get(
                    "price",
                    0
                ),

            "market_price":
                market.get(
                    "market_price",
                    0
                ),

            "difference_percent":
                market.get(
                    "difference_percent",
                    0
                ),

            "price_signal":
                (
                    risk.get(
                        "risk",
                        {}
                    ).get(
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
                risk.get(
                    "risk",
                    {}
                ),

            "duplicates":
                dedup.get(
                    "dedup",
                    {}
                ).get(
                    "duplicates",
                    0
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
                decision or {},

            "explanation":
                explanation.get(
                    "summary",
                    ""
                ),

            "ranking":
                ranking
        }
