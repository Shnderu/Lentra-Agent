from typing import Dict, Any, List


class SignalAuthorityResolver:
    """
    Resolves conflicts between market intelligence signals.

    Core purpose:
    - define priority between competing signals
    - normalize conflicting outputs from pricing / risk / dedup / area layers
    - produce deterministic authority-weighted decision basis

    This is NOT ML.
    This is deterministic policy layer.
    """

    def __init__(self):
        # Higher index = higher authority
        self.priority_order = [
            "fraud_probability",
            "price_market_deviation",
            "duplicate_cluster_size",
            "listing_staleness",
            "area_expat_density",
            "area_internet_quality",
            "price_trend",
            "area_noise_level",
        ]

        self.priority_index = {
            name: i for i, name in enumerate(self.priority_order)
        }

    def resolve(self, signals: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes raw signals from all subsystems and resolves conflicts.

        Args:
            signals: dict of signal_name -> value

        Returns:
            dict with:
                - resolved_signals
                - dominant_signal
                - authority_score
        """

        if not signals:
            return {
                "resolved_signals": {},
                "dominant_signal": None,
                "authority_score": 0.0,
            }

        # Filter known signals only
        filtered = {
            k: v for k, v in signals.items()
            if k in self.priority_index
        }

        if not filtered:
            return {
                "resolved_signals": {},
                "dominant_signal": None,
                "authority_score": 0.0,
            }

        # Determine dominant signal by priority + intensity
        dominant = None
        best_score = -1

        for name, value in filtered.items():
            priority = self.priority_index[name]

            # normalize value to numeric weight if possible
            numeric = self._to_float(value)

            # authority score = priority dominance + signal magnitude
            score = (priority * 10.0) + numeric

            if score > best_score:
                best_score = score
                dominant = name

        return {
            "resolved_signals": filtered,
            "dominant_signal": dominant,
            "authority_score": best_score,
        }

    def _to_float(self, value: Any) -> float:
        """
        Safe numeric normalization for heterogeneous signal types.
        """

        if value is None:
            return 0.0

        if isinstance(value, bool):
            return 1.0 if value else 0.0

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            try:
                return float(value)
            except Exception:
                return 0.0

        if isinstance(value, dict):
            # try common patterns
            for key in ("score", "value", "probability", "risk"):
                if key in value:
                    return self._to_float(value[key])
            return 0.0

        if isinstance(value, list) and value:
            # take strongest element
            return max(self._to_float(v) for v in value)

        return 0.0
