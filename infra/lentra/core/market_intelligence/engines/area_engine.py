from typing import Dict, Any


class AreaEngine:
    """
    V3 SAFE AREA ENGINE

    input:
        accumulated result dict

    output:
        enriched result dict

    Responsibility:
    - use normalized city context
    - provide area intelligence contract
    """

    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}

        city = result.get(
            "city"
        )

        query = result.get(
            "query",
            ""
        )

        if city:
            detected = city

        elif "da nang" in query.lower():
            detected = "da_nang"

        else:
            detected = "unknown"


        result["area"] = {

            "detected": detected,

            "city": detected,

            "status": "ok"
        }

        return result
