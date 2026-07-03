from typing import Dict, Any


class GraphV2Safe:
    """
    SAFE GRAPH V2 STUB

    IMPORTANT:
    - does NOT import market intelligence engines
    - does NOT modify scoring
    - only wraps result for future expansion
    """

    def __init__(self, result: Dict[str, Any], payload: Dict[str, Any]):
        self.result = result
        self.payload = payload

    def build(self) -> Dict[str, Any]:
        return {
            "enabled": True,
            "mode": "safe_stub",
            "result_passthrough": self.result,
            "payload_meta": {
                "graph_v2": self.payload.get("graph_v2", False)
            }
        }


def build_graph_v2(result: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    SAFE ENTRY POINT

    GUARANTEE:
    - never raises
    - never touches engines
    - deterministic passthrough
    """
    try:
        return GraphV2Safe(result, payload).build()
    except Exception:
        return {
            "enabled": False,
            "error": "graph_v2_failed_safe_fallback"
        }
