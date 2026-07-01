from typing import Dict, Any, List


class SignalNormalizer:

    def normalize(self, ui: Dict[str, Any], api: Dict[str, Any]) -> List[Dict[str, Any]]:

        return [
            {
                "name": "price",
                "value": ui.get("price", 0),
                "source": "pricing",
                "weight": 1.0,
                "confidence": 1.0
            },
            {
                "name": "market_price",
                "value": ui.get("market_price", 0),
                "source": "pricing",
                "weight": 1.0,
                "confidence": 1.0
            },
            {
                "name": "deviation_pct",
                "value": ui.get("deviation_pct", 0),
                "source": "pricing",
                "weight": 0.9,
                "confidence": 0.9
            },
            {
                "name": "risk_level",
                "value": ui.get("risk_level", "unknown"),
                "source": "risk",
                "weight": 1.0,
                "confidence": 0.95
            },
            {
                "name": "duplicates",
                "value": ui.get("duplicates", 0),
                "source": "dedup",
                "weight": 0.7,
                "confidence": 0.8
            },
            {
                "name": "area_score",
                "value": api.get("signals", {}).get("area_score", 0),
                "source": "expat",
                "weight": 0.85,
                "confidence": 0.8
            },
            {
                "name": "noise_score",
                "value": api.get("signals", {}).get("noise_score", 0),
                "source": "expat",
                "weight": 0.6,
                "confidence": 0.75
            }
        ]
