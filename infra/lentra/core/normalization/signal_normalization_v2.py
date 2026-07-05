from typing import Dict, Any


class SignalNormalizationV2:

    VERSION = "signal_norm_v2"

    def normalize(self, raw: Dict[str, Any]) -> Dict[str, Any]:

        price = raw.get("price", 0)
        market_price = raw.get("market_price", 1)

        # -------------------------
        # PRICING (single source of truth)
        # -------------------------
        deviation = abs(price - market_price) / max(market_price, 1)

        pricing = {
            "score": max(0.0, min(1.0, 1 - deviation)),
            "direction": "over" if price > market_price else "under",
            "deviation": min(1.0, deviation),
            "confidence": max(0.5, 1.0 - deviation * 0.5)
        }

        # -------------------------
        # GEO (AREA → unified geo model)
        # -------------------------
        area_raw = raw.get("area", {}) or {}

        expat = area_raw.get("expat_density", 0.5)
        tourism = area_raw.get("tourism", 0.5)
        cost = area_raw.get("cost_index", 0.5)

        geo_score = (
            expat * 0.4 +
            tourism * 0.3 +
            cost * 0.3
        )

        geo = {
            "score": max(0.0, min(1.0, geo_score)),
            "city": area_raw.get("city", "unknown"),
            "country": area_raw.get("country", "unknown"),
            "weights": {
                "expat_density": expat,
                "tourism": tourism,
                "cost_index": cost
            },
            "version": "geo_v1"
        }

        # -------------------------
        # RISK (ONLY NORMALIZED VALUE)
        # -------------------------
        risk_raw = raw.get("risk", {}) or {}

        risk = {
            "score": risk_raw.get("risk_level", 0.5),
            "confidence": 1.0 - abs(risk_raw.get("risk_level", 0.5) - 0.5)
        }

        # -------------------------
        # DEDUP
        # -------------------------
        dedup_raw = raw.get("dedup", {}) or {}

        dedup = {
            "score": dedup_raw.get("score", 1.0),
            "confidence": dedup_raw.get("confidence", 1.0)
        }

        return {
            "pricing": pricing,
            "geo": geo,
            "risk": risk,
            "dedup": dedup,
            "_meta": {
                "version": self.VERSION,
                "clean": True
            }
        }
