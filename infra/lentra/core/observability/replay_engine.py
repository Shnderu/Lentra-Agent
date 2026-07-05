from typing import Dict, Any, List, Optional
import copy


class ReplayEngine:
    """
    DEBUG REPLAY MODE (STEP 2.4)

    PURPOSE:
    - replay same request multiple times
    - compare engine outputs
    - detect regression
    - explain ranking changes

    SAFE RULES:
    - NO side effects
    - pure comparison layer
    """

    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    # -------------------------
    # STORE RUN
    # -------------------------
    def store(self, request_id: str, engine_result: Dict[str, Any]) -> None:
        self.history.append({
            "request_id": request_id,
            "result": copy.deepcopy(engine_result)
        })

    # -------------------------
    # REPLAY LAST N
    # -------------------------
    def replay(self, request_id: str, last_n: int = 2) -> Dict[str, Any]:
        runs = [
            h["result"]
            for h in self.history
            if h["request_id"] == request_id
        ]

        if len(runs) < 2:
            return {
                "status": "insufficient_history",
                "request_id": request_id
            }

        runs = runs[-last_n:]

        base = runs[0]
        current = runs[-1]

        diff = self._diff(base, current)

        return {
            "status": "ok",
            "request_id": request_id,
            "comparison": diff,
            "base_version": base.get("ranking", {}).get("version"),
            "current_version": current.get("ranking", {}).get("version"),
        }

    # -------------------------
    # CORE DIFF ENGINE
    # -------------------------
    def _diff(self, base: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:

        return {
            "pricing": self._compare_metric(base, current, "pricing"),
            "risk": self._compare_metric(base, current, "risk"),
            "ranking": self._compare_metric(base, current, "ranking"),
            "coupling": self._compare_metric(base, current, "coupling"),
            "area": self._compare_metric(base, current, "area"),
        }

    # -------------------------
    # METRIC COMPARATOR
    # -------------------------
    def _compare_metric(self, base: Dict[str, Any], current: Dict[str, Any], key: str) -> Dict[str, Any]:

        b = base.get(key)
        c = current.get(key)

        if b is None or c is None:
            return {
                "status": "missing",
                "base": b,
                "current": c
            }

        if isinstance(b, dict) and isinstance(c, dict):

            # numeric score diff
            b_score = b.get("score")
            c_score = c.get("score")

            return {
                "status": "ok",
                "score_diff": self._safe_diff(b_score, c_score),
                "base": b,
                "current": c
            }

        return {
            "status": "non_structured",
            "base": b,
            "current": c
        }

    def _safe_diff(self, a: Optional[float], b: Optional[float]) -> Optional[float]:
        if a is None or b is None:
            return None
        return round(b - a, 6)
