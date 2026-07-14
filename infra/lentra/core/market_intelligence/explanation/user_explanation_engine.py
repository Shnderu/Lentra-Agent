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

        difference = round(
            card.get(
                "difference_percent",
                0
            ),
            2
        )

        risk = card.get(
            "risk",
            {}
        )

        if not isinstance(
            risk,
            dict
        ):
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

        if not isinstance(
            decision,
            dict
        ):
            decision = {}

        action = (
            decision.get("decision")
            or decision.get("action")
            or "REVIEW"
        )

        score = round(
            decision.get(
                "decision_score",
                0
            ) * 100
        )

        saving = max(
            market_price - price,
            0
        )

        overpay = max(
            price - market_price,
            0
        )

        lines = []

        if difference <= -10:

            lines.append(
                f"Цена ниже рынка на {abs(difference)}%."
            )

            if saving > 0:
                lines.append(
                    f"Экономия относительно рынка: {saving:,.0f} VND."
                )

        elif difference >= 10:

            lines.append(
                f"Цена выше рынка на {difference}%."
            )

            if overpay > 0:
                lines.append(
                    f"Потенциальная переплата: {overpay:,.0f} VND."
                )

        else:

            lines.append(
                "Цена находится в рыночном диапазоне."
            )

        lines.append(
            f"Риск объявления: {risk_level}."
        )

        lines.append(
            f"Количество дублей: {duplicates}."
        )

        lines.append(
            f"Рекомендация AI: {action}."
        )

        lines.append(
            f"Уверенность модели: {score}%."
        )

        return "\n".join(lines)
