from typing import Dict, Any
from lentra.core.market_intelligence.graph_v2.graph_builder import build_graph_v2


def apply_graph_v2_contract(result: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    GRAPH V2 ENRICHMENT CONTRACT

    SAFE RULE:
    - never affects scoring
    - only decorates response
    - never blocks engine
    """

    if not payload.get("graph_v2", False):
        return result

    # idempotency guard
    if "graph" in result:
        return result

    try:
        graph = build_graph_v2(result, payload)
        result["graph"] = graph
    except Exception:
        # graph MUST NEVER break system
        pass

    return result
