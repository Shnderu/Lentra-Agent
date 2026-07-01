from typing import Dict, Any, Set


class IntelligenceAudit:

    """
    Анализирует потерю интеллекта между engine_result → output mapping
    """

    def __init__(self):
        self.expected_keys: Set[str] = {
            # PRICE
            "price",
            "market_price",
            "deviation_pct",

            # RISK
            "risk_level",
            "confidence",

            # DEDUP
            "duplicates",

            # AREA
            "area",
            "expat",
            "geo",

            # EXPLANATION
            "explanation",
            "verdict",

            # MARKET DYNAMICS
            "dynamics",
            "trend",
            "volatility",

            # SCORING
            "scores",
            "signals",

            # META
            "source_count",
            "confidence_breakdown",
        }

    def diff(self, engine_result: Dict[str, Any]) -> Dict[str, Any]:

        present_keys = set(engine_result.keys())

        missing = self.expected_keys - present_keys
        unexpected = present_keys - self.expected_keys

        return {
            "missing_intelligence": sorted(list(missing)),
            "unused_engine_output": sorted(list(unexpected)),
            "coverage_pct": self._coverage(present_keys),
        }

    def _coverage(self, present: Set[str]) -> float:
        if not self.expected_keys:
            return 0.0
        return len(present & self.expected_keys) / len(self.expected_keys)
