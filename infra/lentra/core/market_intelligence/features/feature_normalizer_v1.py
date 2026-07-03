from typing import Dict, Any


class FeatureNormalizerV1:
    """
    SAFE NORMALIZATION LAYER (no scoring logic)

    Purpose:
    - unify signals into a single feature contract
    - remove duplication between risk/ranking
    - DO NOT compute any new intelligence
    """

    def normalize(self, signals: Dict[str, Any], raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "price": signals.get("pricing", {}),
            "area": signals.get("area", {}),
            "dedup": signals.get("dedup", {}),
            "coupling": signals.get("coupling", {}),
            "risk": signals.get("risk", {}),
            "raw_context": {
                "query": raw.get("query"),
                "price": raw.get("price"),
                "market_price": raw.get("market_price"),
            }
        }
