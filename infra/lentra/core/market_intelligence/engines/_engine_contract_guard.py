from typing import Dict, Any


def enforce_engine_contract(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    IMMUTABLE ENGINE CONTRACT LAYER

    RULE:
    - ENGINE NEVER RETURNS GRAPH RELATED KEYS
    """

    # HARD STRIP GRAPH KEYS
    result.pop("graph", None)

    # SAFETY: nested graph leaks
    if isinstance(result.get("data"), dict):
        result["data"].pop("graph", None)

    return result
