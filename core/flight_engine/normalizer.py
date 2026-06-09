from typing import Dict, List


class FlightNormalizer:

    @staticmethod
    def normalize(items: List[Dict]) -> List[Dict]:

        normalized = []

        for i in items:
            try:
                normalized.append({
                    "airline": str(i.get("airline")),
                    "price": float(i.get("price", 999999)),
                    "from": i.get("from"),
                    "to": i.get("to"),
                    "date": i.get("date"),
                    "duration": i.get("duration", "N/A"),
                    "provider": i.get("provider", "unknown")
                })
            except Exception:
                continue

        return normalized
