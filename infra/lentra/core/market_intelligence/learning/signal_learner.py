from typing import List, Dict, Any


class SignalLearner:

    def learn(self, history: List[List[Dict[str, Any]]]) -> Dict[str, Any]:

        if len(history) < 2:
            return {
                "weight_updates": {},
                "bias_shift": 0.0,
                "confidence_tuning": 0.0
            }

        last = history[-1]
        prev = history[-2]

        def get(sig_list, name):
            for s in sig_list:
                if s.get("name") == name:
                    return s.get("value")
            return None

        # -------------------------
        # PRICE STABILITY LEARNING
        # -------------------------
        price_curr = get(last, "price")
        price_prev = get(prev, "price")

        price_stable = price_curr == price_prev

        # -------------------------
        # AREA QUALITY LEARNING
        # -------------------------
        area_curr = get(last, "area_score")
        area_prev = get(prev, "area_score")

        area_improving = (
            area_curr is not None and area_prev is not None and area_curr > area_prev
        )

        # -------------------------
        # RISK CONSISTENCY
        # -------------------------
        risk_curr = get(last, "risk_level")
        risk_prev = get(prev, "risk_level")

        risk_stable = risk_curr == risk_prev

        # -------------------------
        # LEARNING OUTPUT
        # -------------------------
        weight_updates = {}

        bias_shift = 0.0
        confidence_tuning = 0.0

        # stable price → reduce sensitivity
        if price_stable:
            weight_updates["price"] = 0.95
            confidence_tuning += 0.02

        # improving area → increase expat importance
        if area_improving:
            weight_updates["area_score"] = 1.1
            bias_shift += 0.05

        # stable risk → increase trust in risk engine
        if risk_stable:
            weight_updates["risk_level"] = 1.05
            confidence_tuning += 0.03

        return {
            "weight_updates": weight_updates,
            "bias_shift": bias_shift,
            "confidence_tuning": confidence_tuning
        }
