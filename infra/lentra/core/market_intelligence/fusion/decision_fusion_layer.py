from typing import Dict, Any


class DecisionFusionLayer:
    """
    SAFE NON-BREAKING FUSION LAYER

    Input:
        graph_result + engines_output

    Output:
        enriched decision payload

    НЕ заменяет decision engine
    НЕ влияет на scoring
    только enrich + explanation
    """

    def __init__(self):
        self.version = "fusion_v1"

    def enrich(
        self,
        engines: Dict[str, Any],
        graph_result: Dict[str, Any],
        payload: Dict[str, Any],
    ) -> Dict[str, Any]:

        pricing = engines.get("pricing", {}).evaluate(payload)
        signal = engines.get("signal", {}).evaluate(payload)

        # graph augmentation (safe read-only)
        graph_score = graph_result.get("signal", {}).get("score", 0)

        base_score = signal.get("score", 0)

        # fusion boost (very conservative)
        fused_score = (base_score * 0.8) + (graph_score * 0.2)

        if fused_score > 0.65:
            decision = "strong_buy"
        elif fused_score > 0.55:
            decision = "buy"
        elif fused_score < 0.35:
            decision = "avoid"
        else:
            decision = "hold"

        explanation = {
            "base_signal": signal,
            "graph_signal": graph_score,
            "fused_score": round(fused_score, 3),
            "decision": decision,
            "reasoning": [
                "signal_engine_primary",
                "graph_enrichment_applied",
                "safe_fusion_v1"
            ]
        }

        return {
            "pricing": pricing,
            "signal": signal,
            "graph": graph_result,
            "decision": explanation,
            "fusion_version": self.version
        }
