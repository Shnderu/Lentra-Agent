from typing import List, Dict, Any


class DecisionFeedbackEngine:

    def evaluate(self, history: List[List[Dict[str, Any]]]) -> Dict[str, Any]:

        if len(history) < 2:
            return {
                "accuracy_score": 0.5,
                "bias_correction": 0.0
            }

        last = history[-1]
        prev = history[-2]

        def get(sig_list, name):
            for s in sig_list:
                if s.get("name") == name:
                    return s.get("value")
            return None

        last_price = get(last, "price")
        prev_price = get(prev, "price")

        last_risk = get(last, "risk_level")
        prev_risk = get(prev, "risk_level")

        accuracy_score = 0.5
        bias_correction = 0.0

        # -------------------------
        # PRICE CONSISTENCY CHECK
        # -------------------------
        if last_price == prev_price:
            accuracy_score += 0.1
        else:
            accuracy_score += 0.05

        # -------------------------
        # RISK CONSISTENCY
        # -------------------------
        if last_risk == prev_risk:
            accuracy_score += 0.1
            bias_correction += 0.02
        else:
            accuracy_score -= 0.05
            bias_correction -= 0.03

        return {
            "accuracy_score": round(accuracy_score, 4),
            "bias_correction": bias_correction
        }
