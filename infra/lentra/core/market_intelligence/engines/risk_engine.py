from typing import Dict, Any, List


class RiskEngine:
    """
    Market Intelligence Risk Engine v2.

    Responsibility:
    - estimate fraud probability
    - separate opportunity from scam risk
    - explain risk signals

    Signals:
    - price anomaly
    - suspicious text
    - source reliability
    """

    SUSPICIOUS_WORDS = [
        "scam",
        "suspicious",
        "urgent",
        "deposit",
        "advance",
        "owner refuses",
        "no viewing",
        "cheap",
    ]

    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}

        price = float(
            result.get(
                "price",
                0
            )
        )

        market = float(
            result.get(
                "market_price",
                0
            )
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

        text = f"{title} {description}"


        if market:

            deviation = (
                price - market
            ) / market

        else:

            deviation = 0.0


        signals: List[str] = []

        fraud_score = 0.1


        # -----------------------------
        # Price anomaly
        # -----------------------------

        if deviation <= -0.40:

            fraud_score += 0.35
            signals.append(
                "extreme_low_price"
            )

        elif deviation <= -0.25:

            fraud_score += 0.20
            signals.append(
                "below_market_price"
            )


        # -----------------------------
        # Text analysis
        # -----------------------------

        for word in self.SUSPICIOUS_WORDS:

            if word in text:

                fraud_score += 0.15

                signals.append(
                    f"text:{word}"
                )


        # -----------------------------
        # Source analysis
        # -----------------------------

        if source == "telegram":

            fraud_score += 0.05

            signals.append(
                "telegram_source"
            )


        if source == "unknown":

            fraud_score += 0.1

            signals.append(
                "unknown_source"
            )


        fraud_score = min(
            fraud_score,
            1.0
        )


        if fraud_score >= 0.7:

            level = "high"

        elif fraud_score >= 0.35:

            level = "medium"

        else:

            level = "low"


        result["risk"] = {

            "fraud_score": round(
                fraud_score,
                4
            ),

            "level": level,

            "signals": signals,

            "price_signal":
                "below_market"
                if deviation < 0
                else "normal",

            "deviation": round(
                deviation,
                4
            ),

            "source": source,

            "status": "ok"
        }


        return result
