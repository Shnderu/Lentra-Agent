from typing import Dict, Any


class UserExplanationEngine:
    """
    Converts internal intelligence signals
    into user-facing rental explanation.

    Compatible with DecisionLayer v2 contract:
    decision:
        {
            "decision": "ACCEPT|REVIEW|REJECT",
            "decision_score": float
        }
    """

    def explain(
        self,
        card: Dict[str, Any]
    ) -> str:

        difference = card.get(
            "difference_percent",
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
            decision.get(
                "decision"
            )
            or
            decision.get(
                "action"
            )
            or
            "REVIEW"
        )

        score = decision.get(
            "decision_score",
            0
        )


        if action == "REJECT":

            return (
                "🔴 Лучше избегать.\n\n"
                "Объявление имеет высокий риск "
                "или низкую рыночную ценность.\n\n"
                f"Уровень уверенности решения: "
                f"{round(score * 100)}%."
            )


        if action == "ACCEPT":

            reasons = []

            if difference < 0:
                reasons.append(
                    f"✓ цена ниже рынка на {abs(difference)}%"
                )

            elif difference <= 5:
                reasons.append(
                    "✓ цена соответствует рынку"
                )

            if risk_level == "low":
                reasons.append(
                    "✓ низкий риск объявления"
                )

            if duplicates == 0:
                reasons.append(
                    "✓ подозрительные дубли не обнаружены"
                )

            return (
                "🟢 Хорошее предложение.\n\n"
                + "\n".join(reasons)
                + "\n\n"
                f"Уверенность решения: {round(score * 100)}%."
            )


        reasons = []

        if difference > 5:
            reasons.append(
                f"Цена выше рынка на {difference}%"
            )
        else:
            reasons.append(
                "Цена находится в рыночном диапазоне"
            )

        if duplicates > 0:
            reasons.append(
                f"Найдено похожих объявлений: {duplicates}"
            )

        if risk_level != "unknown":
            reasons.append(
                f"Риск объявления: {risk_level}"
            )

        return (
            "🟡 Требует проверки.\n\n"
            + "\n".join(reasons)
            + "\n\n"
            f"Уверенность решения: {round(score * 100)}%."
        )
