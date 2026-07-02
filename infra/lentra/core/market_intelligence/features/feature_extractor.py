class FeatureExtractor:
    """
    Converts engine outputs into unified feature space
    """

    def extract(self, engine_outputs: dict) -> dict:
        return {
            "price_delta": engine_outputs.get("pricing", {}).get("delta", 0),
            "risk": engine_outputs.get("risk", {}).get("risk_level", 0.5),
            "signal": engine_outputs.get("signal", {}).get("score", 0.5),
            "dedup_matches": engine_outputs.get("dedup", {}).get("matches", 0),
            "area_score": engine_outputs.get("expat", {}).get("area_score", 0.5),
        }
