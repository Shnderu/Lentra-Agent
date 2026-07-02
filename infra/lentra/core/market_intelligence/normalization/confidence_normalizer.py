class ConfidenceNormalizer:
    """
    Converts raw engine outputs into unified confidence space [0..1]
    """

    def normalize_pricing(self, data: dict) -> float:
        score = data.get("score", 0.5)
        delta = data.get("delta", 0.0)

        # price stability boosts confidence
        stability_boost = max(0.0, 1.0 - abs(delta))

        return min(1.0, max(0.0, 0.6 * score + 0.4 * stability_boost))

    def normalize_risk(self, data: dict) -> float:
        risk = data.get("risk_level", 0.5)
        return 1.0 - risk

    def normalize_signal(self, data: dict) -> float:
        return data.get("score", 0.5)

    def normalize_graph(self, data: dict) -> float:
        # graph is interpretative, lower weight
        return 0.5
