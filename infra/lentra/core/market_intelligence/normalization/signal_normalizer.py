from typing import Dict, Any


class SignalNormalizer:
    """
    Signal Normalization Layer v0.9

    PURPOSE:
    - stabilize signal ranges before ranking
    - prevent engine drift
    - enforce [0..1] bounds
    """

    def normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:

        signals = data.get("signals", {})

        # -----------------------
        # PRICING NORMALIZATION
        # -----------------------
        if "pricing" in signals:
            p = signals["pricing"]
            p["score"] = self._clip(p.get("score", 0.0))
            p["deviation"] = self._clip(p.get("deviation", 0.0))
            p["confidence"] = self._clip(p.get("confidence", 0.0))

        # -----------------------
        # AREA NORMALIZATION
        # -----------------------
        if "area" in signals:
            a = signals["area"]
            a["score"] = self._clip(a.get("score", 0.0))

        # -----------------------
        # COUPLING NORMALIZATION
        # -----------------------
        if "coupling" in signals:
            c = signals["coupling"]
            c["score"] = self._clip(c.get("score", 0.0))

            factors = c.get("factors", {})
            if isinstance(factors, dict):
                for k, v in factors.items():
                    if isinstance(v, (int, float)):
                        factors[k] = self._clip(v)

        # -----------------------
        # RISK NORMALIZATION
        # -----------------------
        if "risk" in data:
            r = data["risk"]
            if "risk_level" in r:
                r["risk_level"] = self._clip(r["risk_level"])

        data["signals"] = signals
        data["risk"] = data.get("risk", {})

        return data

    def _clip(self, v: float) -> float:
        if v is None:
            return 0.0
        if v < 0:
            return 0.0
        if v > 1:
            return 1.0
        return float(v)
