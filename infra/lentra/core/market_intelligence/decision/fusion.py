from typing import Dict, Any

class DecisionFusionLayer:
    """
    SAFE ENRICHMENT LAYER

    НЕ ломает engines
    НЕ участвует в bootstrap
    """

    def fuse(self, gateway_result: Dict[str, Any]) -> Dict[str, Any]:

        signal = gateway_result.get("signal", {})

        confidence = signal.get("score", 0)

        gateway_result["fusion"] = {
            "confidence_band":
                "high" if confidence > 0.7 else
                "medium" if confidence > 0.4 else
                "low",
            "action_weighted": confidence * 1.2
        }

        return gateway_result
