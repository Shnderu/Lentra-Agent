from typing import Dict, Any, List


class RiskEngine:
    """
    Market Intelligence Risk Engine v3.

    Responsibility:
    - estimate fraud probability
    - separate opportunity from scam risk
    - explain risk signals

    Principle:

    Low price is not fraud.

    Fraud requires combination of:
    - extreme anomaly
    - suspicious text
    - unreliable source
    """


    SUSPICIOUS_WORDS = [
        "scam",
        "suspicious",
        "urgent",
        "deposit",
        "advance",
        "owner refuses",
        "no viewing",
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


        deviation = 0.0

        if market:

            deviation = (
                price - market
            ) / market


        signals: List[str] = []

        fraud_score = 0.1


        opportunity_signals = []


        # =========================
        # PRICE INTELLIGENCE
        # =========================

        if deviation <= -0.50:

            fraud_score += 0.20

            signals.append(
                "extreme_low_price"
            )


        elif deviation <= -0.25:

            opportunity_signals.append(
                "below_market_price"
            )


        # =========================
        # TEXT RISK
        # =========================

        for word in self.SUSPICIOUS_WORDS:

            if word in text:

                fraud_score += 0.20

                signals.append(
                    f"text:{word}"
                )


        # =========================
        # SOURCE RISK
        # =========================

        if source == "unknown":

            fraud_score += 0.15

            signals.append(
                "unknown_source"
            )


        elif source == "telegram":

            fraud_score += 0.05

            signals.append(
                "telegram_source"
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

            "fraud_score":
                round(
                    fraud_score,
                    4
                ),

            "level":
                level,

            "signals":
                signals,

            "opportunity_signals":
                opportunity_signals,

            "price_signal":
                (
                    "below_market"
                    if deviation < 0
                    else "normal"
                ),

            "deviation":
                round(
                    deviation,
                    4
                ),

            "source":
                source,

            "status":
                "ok"

        }


        return result
