from typing import Dict, Any, List


class RiskEngine:
    """
    Canonical Market Intelligence Risk Engine.

    Responsibility:

    - fraud probability
    - listing reliability
    - market anomaly explanation

    Output contract:

    {
        risk_score,
        risk_level,
        signals,
        opportunity_signals
    }

    Low price != fraud.
    """


    SUSPICIOUS_WORDS = [
        "scam",
        "urgent",
        "deposit",
        "advance",
        "no viewing",
        "owner refuses"
    ]


    def run(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}


        price = float(
            result.get(
                "price",
                0
            ) or 0
        )


        market = float(
            result.get(
                "market_price",
                0
            ) or 0
        )


        source = result.get(
            "source",
            "unknown"
        )


        title = str(
            result.get(
                "title",
                ""
            )
        ).lower()


        description = str(
            result.get(
                "description",
                ""
            )
        ).lower()


        text = (
            f"{title} {description}"
        )


        score = 0.1


        signals: List[str] = []

        opportunity_signals = []


        deviation = 0.0


        if market:

            deviation = (
                price - market
            ) / market


            if deviation <= -0.50:

                score += 0.25

                signals.append(
                    "extreme_low_price"
                )


            elif deviation <= -0.25:

                opportunity_signals.append(
                    "below_market_price"
                )


        for word in self.SUSPICIOUS_WORDS:

            if word in text:

                score += 0.20

                signals.append(
                    f"text:{word}"
                )


        if source == "unknown":

            score += 0.15

            signals.append(
                "unknown_source"
            )


        elif source == "telegram":

            score += 0.05

            signals.append(
                "telegram_source"
            )


        if not result.get("contact"):

            score += 0.05

            signals.append(
                "missing_contact"
            )


        if not result.get("images"):

            score += 0.03

            signals.append(
                "missing_images"
            )


        score = min(
            score,
            1.0
        )


        if score >= 0.7:

            level = "high"

        elif score >= 0.35:

            level = "medium"

        else:

            level = "low"



        return {

            **result,

            "risk_score": round(
                score,
                4
            ),

            "risk_level": level,

            "risk_signals": signals,

            "risk_opportunity_signals": opportunity_signals,

            "risk_deviation": round(
                deviation,
                4
            )

        }
