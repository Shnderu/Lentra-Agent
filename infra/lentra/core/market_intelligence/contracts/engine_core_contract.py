from typing import Dict, Any


def enforce_engine_core_contract(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    DEEP IMMUTABLE CORE CONTRACT

    RULE:
    - ENGINE OUTPUT IS PURE PRIMITIVE INTELLIGENCE ONLY
    - NO POST-PROCESS FEATURES ALLOWED
    """

    # HARD STRIP ALL NON-CORE FIELDS
    forbidden_keys = {
        "graph",
        "visual",
        "chart",
        "ui",
        "enrichment",
        "presentation"
    }

    for k in list(result.keys()):
        if k in forbidden_keys:
            result.pop(k, None)

    # deep safety
    if isinstance(result.get("data"), dict):
        for k in list(result["data"].keys()):
            if k in forbidden_keys:
                result["data"].pop(k, None)

    return result
