from typing import Dict, Any


class DecisionLayer:
    """
    Decision Layer v2.0

    PRINCIPLE:

    - Risk has authority over ranking
    - Ranking selects quality among trusted objects
    - Decision layer only aggregates intelligence signals

    Order:

    Risk Gate
        |
        v
    Pricing + Area Intelligence
        |
        v
    Ranking
        |
        v
    Final Decision
    """


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


        # =========================
        # RISK AUTHORITY GATE
        # =========================

        if risk_score >= 0.7:

            return {

                "decision": "REJECT",

                "decision_score": round(
                    1 - risk_score,
                    4
                ),

                "components": {

                    "ranking": ranking_score,

                    "pricing": pricing_score,

                    "area": area_score,

                    "risk": risk_score

                },

                "reason": "Высокий риск объявления.",

                "signals": signals,

                "risk": risk,

                "ranking": ranking

            }


        if risk_score >= 0.45:

            return {

                "decision": "REVIEW",

                "decision_score": round(
                    (
                        pricing_score * 0.4
                        +
                        area_score * 0.2
                        +
                        ranking_score * 0.2
                        +
                        (1 - risk_score) * 0.2
                    ),
                    4
                ),

                "components": {

                    "ranking": ranking_score,

                    "pricing": pricing_score,

                    "area": area_score,

                    "risk": risk_score

                },

                "reason": "Средний риск. Требуется проверка.",

                "signals": signals,

                "risk": risk,

                "ranking": ranking

            }


        # =========================
        # TRUSTED OBJECT SCORING
        # =========================

        final_score = (

            pricing_score * 0.40

            +

            area_score * 0.20

            +

            ranking_score * 0.25

            +

            (1 - risk_score) * 0.15

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

                "risk": risk_score

            },

            "reason": "Решение сформировано по модели доверия и рыночной ценности.",

            "signals": signals,

            "risk": risk,

            "ranking": ranking

        }
