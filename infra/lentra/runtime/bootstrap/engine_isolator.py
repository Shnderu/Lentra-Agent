from typing import Dict, Any


class EngineIsolator:
    """
    Contract Stabilization Layer v2

    PRINCIPLE:
    - compute() is single source of truth
    - isolator is ONLY orchestration layer
    - AreaEngine is externalized (SEA expansion)
    """

    def __init__(self, engines: Dict[str, Any]):
        self.engines = engines or {}

    def run_all(self, payload: Dict[str, Any]) -> Dict[str, Any]:

        engine = self.engines.get("market_intelligence")

        if engine is None:
            return {
                "dedup": {},
                "ranking": {},
                "risk": {},
                "signals": {},
                "features": {},
                "decision": {
                    "decision": "NO_ENGINE"
                }
            }

        # =========================
        # CORE MI ENGINE
        # =========================
        result = engine.compute(payload)

        # =========================
        # AREA ENGINE (SEA ISOLATION LAYER)
        # =========================
        area_engine = self.engines.get("area")

        if area_engine is not None:
            try:
                area_result = area_engine.compute(payload)

                if "signals" not in result:
                    result["signals"] = {}

                result["signals"]["area"] = area_result

                # lightweight coupling boost from geography
                if "coupling" in result.get("signals", {}):
                    result["signals"]["coupling"]["area_boost"] = area_result.get("score", 0.5)

            except Exception:
                # fail-safe: area never breaks pipeline
                pass

        # =========================
        # CONTRACT FREEZE LAYER
        # =========================
        if isinstance(result, dict):
            result.setdefault("dedup", {})
            result.setdefault("ranking", {})
            result.setdefault("risk", {})
            result.setdefault("signals", {})
            result.setdefault("features", {})
            result.setdefault("decision", {})

        return result
