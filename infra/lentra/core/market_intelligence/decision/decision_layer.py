from typing import Dict, Any

from lentra.core.market_intelligence.segments.segment_signal import SegmentSignalAdapter


class DecisionLayer:
    """
    Decision Layer v2.3

    Single authority for final market intelligence decision.

    Responsibilities:
    - aggregate market signals
    - apply risk authority gate
    - combine ranking, pricing, area and segment signals
    """


    def build_from_signals(
        self,
        market: Dict[str, Any],
        risk: Dict[str, Any],
        area: Dict[str, Any],
        ranking_score: float = 0.5,
        segment_market: Dict[str, Any] = None,
    ) -> Dict[str, Any]:

        segment_signal = SegmentSignalAdapter().build(
            market.get(
                "price",
                0
            ),
            segment_market or {}
        )


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
                    "area": area,
                    "segment_market": segment_market or {}
                },

                "ranking": {
                    "score": ranking_score
                },

                "risk": {
                    "risk_level": fraud_score
                },

                "segment_signal": segment_signal
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

        segment_signal = data.get(
            "segment_signal",
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

        segment_market = signals.get(
            "segment_market",
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


        segment_confidence = segment_signal.get(
            "confidence",
            0.0
        )


        segment_status = segment_signal.get(
            "status",
            "unknown"
        )


        segment_bonus = 0.0


        if (
            segment_status == "premium"
            and segment_confidence >= 0.3
        ):

            segment_bonus = (
                segment_confidence * 0.05
            )


        elif (
            segment_status == "standard"
            and segment_confidence >= 0.5
        ):

            segment_bonus = (
                segment_confidence * 0.02
            )


        segment_position = segment_signal.get(
            "position",
            "unknown"
        )


        if segment_position == "below_segment_market":

            segment_position_bonus = 0.05

        elif segment_position == "above_segment_market":

            segment_position_bonus = -0.05

        else:

            segment_position_bonus = 0.0


        difference_percent = pricing.get(
            "difference_percent",
            0
        )


        price_direction = pricing.get(
            "direction",
            "unknown"
        )


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

                "reason":
                    "Высокий риск объявления.",

                "segment_confidence":
                    round(
                        segment_confidence,
                        3
                    ),

                "segment_market":
                    segment_market,

                "segment_signal":
                    segment_signal,

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

                (1-risk_score) * 0.2

                +

                segment_bonus

                +

                segment_position_bonus

            )


            return {

                "decision": "REVIEW",

                "decision_score":
                    round(
                        score,
                        4
                    ),

                "reason":
                    "Средний риск. Требуется проверка.",

                "segment_confidence":
                    round(
                        segment_confidence,
                        3
                    ),

                "segment_market":
                    segment_market,

                "segment_signal":
                    segment_signal,

                "signals": signals,

                "risk": risk,

                "ranking": ranking

            }


        if opportunity_gate:

            return {

                "decision": "ACCEPT",

                "decision_score": 0.85,

                "reason":
                    "Цена значительно ниже рынка при низком риске.",

                "segment_confidence":
                    round(
                        segment_confidence,
                        3
                    ),

                "segment_market":
                    segment_market,

                "segment_signal":
                    segment_signal,

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

            (1-risk_score) * 0.20

            +

            segment_bonus

        )


        return {

            "decision": "WATCH",

            "decision_score":
                round(
                    final_score,
                    4
                ),

            "reason":
                "Объект соответствует рынку.",

            "segment_confidence":
                round(
                    segment_confidence,
                    3
                ),

            "segment_market":
                segment_market,

            "signals":
                signals,

            "risk":
                risk,

            "ranking":
                ranking

        }
