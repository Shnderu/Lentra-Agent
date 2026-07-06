class RiskEngine:

    # shared thresholds so evaluate() and apply_dedup_signal() stay consistent
    HIGH_THRESHOLD = 0.7
    MEDIUM_THRESHOLD = 0.3

    def _clamp(self, value: float) -> float:
        # risk score is always expressed in the [0.0, 1.0] range
        return max(0.0, min(1.0, value))

    def _level_from_score(self, risk_score: float) -> str:
        if risk_score > self.HIGH_THRESHOLD:
            return "high"
        elif risk_score > self.MEDIUM_THRESHOLD:
            return "medium"
        return "low"

    def evaluate(self, payload: dict) -> dict:

        payload = payload or {}

        # Derive a base risk from the signals available in the payload
        # instead of hard-coding 0.0. Every component is optional and
        # defended with .get() so partial payloads never raise.
        base_risk = 0.0

        # explicit anomaly signal (already normalized 0..1 upstream)
        base_risk += float(payload.get("anomaly_score", 0.0))

        # market volatility contributes proportionally
        base_risk += 0.3 * float(payload.get("volatility", 0.0))

        # strong deviation from the market baseline raises risk
        price = payload.get("price")
        baseline = payload.get("baseline")
        if price is not None and baseline:
            deviation = abs(float(price) - float(baseline)) / float(baseline)
            base_risk += 0.2 * min(deviation, 1.0)

        risk_score = self._clamp(round(base_risk, 4))

        return {
            "risk_score": risk_score,
            "risk_level": self._level_from_score(risk_score)
        }

    def apply_dedup_signal(self, risk: dict, dedup_result: dict) -> dict:

        duplicates = dedup_result.get("duplicates", 0)
        items = dedup_result.get("items", [])

        cluster_pressure = 0

        if items:
            cluster_pressure = max(
                i.get("cluster_size", 1) for i in items
            ) / 5

        duplication_risk_boost = min(
            0.4 * cluster_pressure + 0.1 * duplicates,
             0.5
        )

        risk_score = self._clamp(
            risk.get("risk_score", 0.0) + duplication_risk_boost
        )

        return {
            **risk,
            "risk_score": round(risk_score, 4),
            "risk_level": self._level_from_score(risk_score),
            "duplication_boost": duplication_risk_boost
        }
