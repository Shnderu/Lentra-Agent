
class ConfidenceEngine:

    def run(self, objects):

        for obj in objects:

            # базовая эвристика
            risk_factor = getattr(obj, "risk", 0.5)
            area_factor = getattr(obj, "area_score", 5.0) / 10.0

            obj.confidence = round(
                max(0.1, min(1.0, (1 - risk_factor) * 0.6 + area_factor * 0.4)),
                2
            )

        return objects
