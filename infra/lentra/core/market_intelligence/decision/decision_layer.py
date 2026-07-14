from typing import Dict, Any


class DecisionLayer:
    """
    Decision Layer v2.2

    Single authority for final market intelligence decision.

    Responsibilities:
    - aggregate market signals
    - apply risk authority gate
    - combine ranking, pricing and area signals
    """


    def build_from_signals(
        self,
        market: Dict[str, Any],
        risk: Dict[str, Any],
        area: Dict[str, Any],
        ranking_score: float = 0.5,
    ) -> Dict[str, Any]:

        risk_data = risk.get(
            "risk",
            {}
        )

        fraud_score = risk_data.get(
            "fraud_score",
            0.5
        )

        return self.build(
            {
                "signals": {
                    "pricing": market,
                    "area": area
                },

                "ranking": {
                    "score": ranking_score
                },

                "risk": {
                    "risk_level": fraud_score
                }
            }
        )


    def build(
        self,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:

        signals = data.get(
            "signals",
            {}
        )

        ranking = data.get(
            "ranking",
            {}
        )

        risk = data.get(
            "risk",
            {}
        )


        pricing = signals.get(
            "pricing",
            {}
        )

        area = signals.get(
            "area",
            {}
        )


        pricing_score = pricing.get(
            "pricing_score",
            0.5
        )

        area_score = area.get(
            "score",
            0.5
        )

        risk_score = risk.get(
            "risk_level",
            0.5
        )

        ranking_score = ranking.get(
            "score",
            0.5
        )


        difference_percent = pricing.get(
            "difference_percent",
            0
        )

        price_direction = pricing.get(
            "direction",
            "unknown"
        )


        opportunity_bonus = 0.0


        if (
            price_direction == "under"
            and difference_percent <= -25
        ):
            opportunity_bonus = 0.15

        elif (
            price_direction == "under"
            and difference_percent <= -10
        ):
            opportunity_bonus = 0.07


        opportunity_gate = (

            price_direction == "under"

            and difference_percent <= -25

            and risk_score < 0.3

        )



        if risk_score >= 0.7:

            return {

                "decision": "REJECT",

                "decision_score": round(
                    1 - risk_score,
                    4
                ),

                "reason": "Высокий риск объявления.",

                "components": {

                    "ranking": ranking_score,
                    "pricing": pricing_score,
                    "area": area_score,
                    "risk": risk_score

                },

                "signals": signals,
                "risk": risk,
                "ranking": ranking

            }



        if risk_score >= 0.45:

            score = (
                pricing_score * 0.4
                +
                area_score * 0.2
                +
                ranking_score * 0.2
                +
                (1 - risk_score) * 0.2
            )


            return {

                "decision": "REVIEW",

                "decision_score": round(
                    score,
                    4
                ),

                "reason": "Средний риск. Требуется проверка.",

                "components": {

                    "ranking": ranking_score,
                    "pricing": pricing_score,
                    "area": area_score,
                    "risk": risk_score

                },

                "signals": signals,
                "risk": risk,
                "ranking": ranking

            }



        if opportunity_gate:

            return {

                "decision": "ACCEPT",

                "decision_score": round(
                    max(
                        final_score if "final_score" in locals() else 0.75,
                        0.75
                    ),
                    4
                ),

                "reason":
                    "Цена значительно ниже рынка при низком риске объявления.",

                "components": {

                    "ranking": ranking_score,
                    "pricing": pricing_score,
                    "area": area_score,
                    "risk": risk_score,
                    "opportunity_bonus": opportunity_bonus

                },

                "signals": signals,
                "risk": risk,
                "ranking": ranking

            }



        final_score = (

            pricing_score * 0.35

            +

            area_score * 0.20

            +

            ranking_score * 0.25

            +

            (1 - risk_score) * 0.15

            +

            opportunity_bonus

        )


        if final_score >= 0.75:
            decision = "ACCEPT"

        elif final_score >= 0.5:
            decision = "REVIEW"

        else:
            decision = "REJECT"


        return {

            "decision": decision,

            "decision_score": round(
                final_score,
                4
            ),

            "components": {

                "ranking": ranking_score,
                "pricing": pricing_score,
                "area": area_score,
                "risk": risk_score,
                "opportunity_bonus": opportunity_bonus

            },

            "reason":
                "Решение сформировано по модели доверия и рыночной ценности.",

            "signals": signals,
            "risk": risk,
            "ranking": ranking

        }
