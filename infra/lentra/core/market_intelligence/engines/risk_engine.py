from typing import Dict, Any, List


class RiskEngine:
    """
    Market Intelligence Risk Engine v4.

    Responsibility:
    - estimate fraud probability
    - explain risk signals
    - combine price, source, content and data quality signals

    Principle:

    Low price is not fraud.

    Fraud requires combination of:
    - extreme anomaly
    - suspicious text
    - unreliable source
    - weak listing quality
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
            or 0
        )


        market = float(
            result.get(
                "market_price",
                0
            )
            or 0
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


        duplicate_count = int(
            result.get(
                "duplicate_count",
                0
            )
            or 0
        )


        deviation = 0.0

        if market > 0:

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


        # =========================
        # LISTING QUALITY
        # =========================

        if not result.get("contact"):

            fraud_score += 0.05

            signals.append(
                "missing_contact"
            )


        if not result.get("images"):

            fraud_score += 0.03

            signals.append(
                "missing_images"
            )


        if price <= 0:

            fraud_score += 0.10

            signals.append(
                "missing_price"
            )


        # =========================
        # DUPLICATE INTELLIGENCE
        # =========================

        if duplicate_count >= 2:

            opportunity_signals.append(
                "verified_multiple_sources"
            )

            fraud_score -= 0.05


        fraud_score = max(
            0.0,
            min(
                fraud_score,
                1.0
            )
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

            "duplicate_count":
                duplicate_count,

            "status":
                "ok"

        }


        return result
