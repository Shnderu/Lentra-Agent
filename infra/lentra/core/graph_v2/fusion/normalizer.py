class FusionNormalizer:
    """
    Stabilizes multi-engine outputs into consistent structure
    """

    def normalize(self, outputs: dict) -> dict:
        return {
            "pricing": outputs.get("pricing", {}),
            "risk": outputs.get("risk", {}),
            "dedup": outputs.get("dedup", {}),
            "expat": outputs.get("expat", {}),
            "graph": outputs  # safe passthrough layer
        }
