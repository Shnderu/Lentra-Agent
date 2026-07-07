from typing import Dict, Any


class DedupEngine:
    """
    V3 DEDUP CONTRACT

    Current stage:
    - contract preparation
    - no external index yet

    Future:
    - object fingerprint
    - source matching
    - duplicate grouping
    - canonical listing selection
    """

    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}


        result["dedup"] = {

            # current safe state
            "duplicates": 0,

            "confidence": 0.0,

            "sources": [],

            "canonical_listing": None,

            "status": "no_index"
        }


        return result
