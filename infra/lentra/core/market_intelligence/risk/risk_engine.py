class RiskEngine:

    def evaluate(self, payload: dict) -> dict:

        price = payload.get("price", 0)

        # minimal sane heuristic baseline
        risk_score = 0.0

        if price > 1000:
            risk_score += 0.2

        if price == 0:
            risk_score += 0.3

        risk_level = "low"
        if risk_score > 0.7:
            risk_level = "high"
        elif risk_score > 0.3:
            risk_level = "medium"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level
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

        risk_score = risk.get("risk_score", 0.0) + duplication_risk_boost

        if risk_score > 0.7:
            risk_level = "high"
        elif risk_score > 0.3:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            **risk,
            "risk_score": round(risk_score, 4),
            "risk_level": risk_level,
            "duplication_boost": duplication_risk_boost
        }
