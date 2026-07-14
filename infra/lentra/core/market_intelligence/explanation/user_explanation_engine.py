from typing import Dict, Any


class UserExplanationEngine:
    """
    Converts internal intelligence signals
    into user-facing rental explanation.

    Contract:
    - DecisionLayer v2
    - ObjectIntelligenceCard
    - Product user explanation
    """

    def explain(
        self,
        card: Dict[str, Any]
    ) -> str:

        difference = card.get(
            "difference_percent",
            0
        )

        saving_amount = card.get(
            "saving_amount",
            0
        )

        risk = card.get(
            "risk",
            {}
        )

        if not isinstance(risk, dict):
            risk = {}

        risk_level = risk.get(
            "level",
            "unknown"
        )

        duplicates = card.get(
            "duplicates",
            0
        )

        decision = card.get(
            "decision",
            {}
        )

        if not isinstance(decision, dict):
            decision = {}

        action = (
            decision.get("decision")
            or
            decision.get("action")
            or
            "REVIEW"
        )

        score = decision.get(
            "decision_score",
            0
        )


        confidence = round(
            score * 100
        )


        if action == "ACCEPT":

            reasons = []


            if difference < 0:

                reasons.append(
                    f"✓ цена ниже рынка на {abs(difference)}%"
                )


            if saving_amount > 0:

                reasons.append(
                    f"✓ экономия относительно рынка: "
                    f"{saving_amount:,.0f} VND"
                )


            if risk_level == "low":

                reasons.append(
                    "✓ низкий риск объявления"
                )


            if duplicates == 0:

                reasons.append(
                    "✓ дубли не обнаружены"
                )


            return (
                "🟢 Хорошее предложение.\n\n"
                +
                "\n".join(reasons)
                +
                "\n\n"
                "Рекомендация: проверить владельца "
                "и документы перед оплатой.\n\n"
                f"Уверенность модели: {confidence}%."
            )


        if action == "REJECT":

            return (
                "🔴 Не рекомендуется.\n\n"
                "Объявление имеет высокий риск "
                "или недостаточную рыночную ценность.\n\n"
                f"Уверенность модели: {confidence}%."
            )


        reasons = []


        if difference > 5:

            reasons.append(
                f"Цена выше рынка на {difference}%"
            )

        elif difference < -5:

            reasons.append(
                f"Цена ниже рынка на {abs(difference)}%"
            )

        else:

            reasons.append(
                "Цена соответствует рынку"
            )


        if risk_level != "unknown":

            reasons.append(
                f"Риск объявления: {risk_level}"
            )


        if duplicates > 0:

            reasons.append(
                f"Найдено похожих объявлений: {duplicates}"
            )


        return (
            "🟡 Требует проверки.\n\n"
            +
            "\n".join(reasons)
            +
            "\n\n"
            f"Уверенность модели: {confidence}%."
        )
