import random
import math


class PredictionEngineV1:

    def predict_price(self, listing):

        base = listing.get("market_price", listing.get("price", 0))
        segment = listing.get("location", {}).get("segment", "unknown")

        # simple geo multipliers (v1 heuristic model)
        multipliers = {
            "beach": 1.12,
            "city": 1.08,
            "suburb": 0.92,
            "unknown": 1.0
        }

        m = multipliers.get(segment, 1.0)

        predicted = base * m

        # noise simulation (v1 stability model)
        noise = random.uniform(-0.03, 0.03)
        predicted = predicted * (1 + noise)

        return {
            "predicted_price": round(predicted, 2),
            "confidence": round(0.7 - abs(noise), 3),
            "model": "prediction_v1"
        }
