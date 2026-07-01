from typing import Dict, Any


class SignalNormalizer:
    """
    Normalizes raw engine outputs into unified SignalContract format.
    """

    def normalize(self, ui: dict, api: dict, meta: dict) -> dict:
        vector = api.get("vector", {})

        return {
            "ui": ui,
            "api": api,
            "normalized": {
                "price": ui.get("price"),
                "market_price": ui.get("market_price"),
                "deviation_pct": ui.get("deviation_pct"),

                "risk_level": ui.get("risk_level"),
                "risk_score": vector.get("risk_signal", {}).get("risk_score", 0.0),

                "duplicates": ui.get("duplicates", 0),

                "area_score": vector.get("area_signal", 0.0),
                "internet_score": vector.get("expat_signal", {}).get("internet_score", 0.0),
                "noise_score": vector.get("noise_signal", 0.0),

                "verdict": ui.get("verdict"),
            },
            "meta": meta,
        }
