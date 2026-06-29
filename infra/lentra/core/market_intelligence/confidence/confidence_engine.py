class ConfidenceEngine:

    def run(self, obj):

        def safe_float(v, default):
            if v is None:
                return default
            try:
                return float(v)
            except Exception:
                return default

        if isinstance(obj, dict):
            risk = safe_float(obj.get("risk"), 0.5)
        else:
            risk = safe_float(getattr(obj, "risk", None), 0.5)

        base = 1.0 - risk

        base = max(0.0, min(1.0, base))

        if isinstance(obj, dict):
            obj["confidence"] = round(base, 3)
        else:
            obj.confidence = round(base, 3)

        return obj
