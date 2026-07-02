class DecisionFusionLayer:
    """
    SAFE ENRICHMENT LAYER

    НЕ заменяет engines
    НЕ меняет graph
    только добавляет decision signal
    """

    def merge(self, graph_result: dict) -> dict:

        signal = graph_result.get("signal", {})

        score = signal.get("score", 0.5)

        if score > 0.75:
            verdict = "buy"
        elif score < 0.4:
            verdict = "avoid"
        else:
            verdict = "neutral"

        graph_result["decision"] = {
            "score": score,
            "verdict": verdict,
            "mode": "fusion_v1"
        }

        return graph_result
