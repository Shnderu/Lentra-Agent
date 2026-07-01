from typing import Dict, Any, List


class WeightGovernor:

    def adjust(self, signals: List[Dict[str, Any]], conflicts: List[str]) -> List[Dict[str, Any]]:

        adjusted = []

        conflict_set = set(conflicts)

        for s in signals:
            weight = s.get("weight", 1.0)

            name = s.get("name")

            # -------------------------
            # PRICE SENSITIVITY
            # -------------------------
            if name == "price":
                if "overprice_low_area" in conflict_set:
                    weight *= 0.7

                if "cheap_scam_signal" in conflict_set:
                    weight *= 0.6

            # -------------------------
            # EXPAT IMPORTANCE SHIFT
            # -------------------------
            if name == "area_score":
                if "expat_risk_buffer" in conflict_set:
                    weight *= 1.3

            # -------------------------
            # NOISE REDUCTION
            # -------------------------
            if name == "duplicates":
                if "high_duplication_noise" in conflict_set:
                    weight *= 0.5

            adjusted.append({
                **s,
                "weight": round(weight, 4)
            })

        return adjusted
