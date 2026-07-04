from typing import Any, Dict


class FeatureGovernanceV2:
    """
    Schema Lock Expansion v1.0

    Goals:
    - enforce signals schema
    - enforce features parity
    - eliminate drift between layers
    """

    VERSION = "schema_lock_v1"

    def enforce(self, data: Dict[str, Any]) -> Dict[str, Any]:
        signals = data.get("signals", {})
        features = data.get("features", {})

        # 1. lock signals schema
        signals = self._lock_signals(signals)

        # 2. rebuild features from signals (source of truth)
        features = self._build_features(signals, data)

        data["signals"] = signals
        data["features"] = features

        data["_schema_lock"] = {
            "version": self.VERSION
        }

        return data

    def _lock_signals(self, s: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "pricing": self._safe(s.get("pricing", {}), {
                "score": 0.0,
                "direction": "ok",
                "deviation": 0.0
            }),
            "area": self._safe(s.get("area", {}), {
                "score": 0.0,
                "note": ""
            }),
            "dedup": self._safe(s.get("dedup", {}), {
                "score": 1.0,
                "confidence": 1.0
            }),
            "coupling": self._safe(s.get("coupling", {}), {
                "score": 0.0,
                "factors": {}
            }),
            "risk": self._safe(s.get("risk", {}), {
                "risk_level": 0.0,
                "score": 0.0,
                "level": "low",
                "components": {}
            }),
            "ranking": self._safe(s.get("ranking", {}), {
                "score": 0.0,
                "components": {},
                "version": "ranking_v2"
            })
        }

    def _build_features(self, signals: Dict[str, Any], raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "price": signals["pricing"],
            "area": signals["area"],
            "dedup": signals["dedup"],
            "coupling": signals["coupling"],
            "risk": signals["risk"],
            "raw_context": {
                "query": raw.get("query"),
                "price": raw.get("price"),
                "market_price": raw.get("market_price")
            }
        }

    def _safe(self, obj: Dict[str, Any], defaults: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(obj, dict):
            obj = {}
        return {k: obj.get(k, v) for k, v in defaults.items()}
