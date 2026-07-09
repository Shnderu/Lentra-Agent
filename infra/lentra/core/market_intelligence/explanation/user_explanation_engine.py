from typing import Dict, Any


class UserExplanationEngine:
    """
    Converts internal intelligence signals
    into user-facing rental explanation.
    """

    def explain(
        self,
        card: Dict[str, Any]
    ) -> str:

        price = card.get(
            "price",
            0
        )

        market_price = card.get(
            "market_price",
            0
        )

        difference = card.get(
            "difference_percent",
            0
        )

        risk = card.get(
            "risk",
            {}
        )

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

        action = decision.get(
            "action",
            "REVIEW"
        )


        if action == "REJECT":

            return (
                "🔴 Лучше избегать.\n\n"
                "Объявление имеет высокий риск. "
                "Не рекомендуется без проверки владельца "
                "и просмотра объекта."
            )


        if action == "ACCEPT":

            reasons = []

            if difference < 0:
                reasons.append(
                    f"✓ цена ниже рынка на {abs(difference)}%"
                )

            if risk_level == "low":
                reasons.append(
                    "✓ низкий риск объявления"
                )

            if duplicates == 0:
                reasons.append(
                    "✓ не найдено подозрительных дублей"
                )

            return (
                "🟢 Хорошее предложение.\n\n"
                + "\n".join(reasons)
                + "\n\n"
                "Рекомендуется проверить объект перед оплатой."
            )


        reasons = []

        if difference > 5:
            reasons.append(
                f"Цена выше рынка на {difference}%"
            )
        else:
            reasons.append(
                "Цена соответствует рынку"
            )

        if duplicates > 0:
            reasons.append(
                f"Найдено похожих объявлений: {duplicates}"
            )

        return (
            "🟡 Требует проверки.\n\n"
            + "\n".join(reasons)
            + "\n\n"
            "Перед арендой стоит сравнить альтернативы."
        )
