from typing import Dict, Any, List


class ExplanationEngine:
    """
    VIETNAM MARKET EXPLANATION LAYER

    Purpose:
    - translate signals into human-readable reasoning
    - no computation, only interpretation
    """

    def explain(self, item: Dict[str, Any]) -> Dict[str, Any]:

        reasons = []

        # -------------------------
        # PRICE EXPLANATION
        # -------------------------
        deviation = item.get("deviation_pct")

        if deviation is not None:
            if abs(deviation) > 40:
                reasons.append("Цена значительно отклоняется от рыночного уровня")
            elif abs(deviation) > 20:
                reasons.append("Цена заметно отличается от среднего по району")
            else:
                reasons.append("Цена близка к рыночному уровню")

        # -------------------------
        # RISK EXPLANATION
        # -------------------------
        risk_score = item.get("risk_score", 0)

        if risk_score >= 70:
            reasons.append("Высокий риск объявления (множественные подозрительные сигналы)")
        elif risk_score >= 40:
            reasons.append("Средний уровень риска (есть настораживающие признаки)")
        else:
            reasons.append("Низкий риск объявления")

        # -------------------------
        # DUPLICATION CONTEXT
        # -------------------------
        duplicates = item.get("duplicate_count")

        if duplicates:
            if duplicates >= 5:
                reasons.append("Объект массово дублируется в источниках")
            elif duplicates >= 3:
                reasons.append("Объект встречается в нескольких источниках")

        # -------------------------
        # FINAL SUMMARY
        # -------------------------
        summary = self._compose_summary(item, reasons)

        return {
            "reasons": reasons,
            "summary": summary
        }

    def _compose_summary(self, item: Dict[str, Any], reasons: List[str]) -> str:

        title = item.get("title", "Объект недвижимости")

        if not reasons:
            return f"{title}: недостаточно данных для анализа"

        return f"{title}: " + "; ".join(reasons)
