class DecisionEngineV2:
    """
    Weighted fusion decision engine
    """

    def decide(self, conf: dict, graph: dict) -> dict:

        score = (
            conf.get("pricing", 0.5) * 0.35 +
            conf.get("risk", 0.5) * 0.35 +
            conf.get("signal", 0.5) * 0.2 +
            conf.get("graph", 0.5) * 0.1
        )

        if score > 0.7:
            verdict = "buy"
        elif score < 0.4:
            verdict = "avoid"
        else:
            verdict = "neutral"

        return {
            "score": score,
            "verdict": verdict,
        }
