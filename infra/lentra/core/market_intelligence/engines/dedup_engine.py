from typing import Dict, Any
import hashlib


class DedupEngine:
    """
    V3 DEDUP CONTRACT

    Responsibility:
    - create object fingerprint
    - prepare duplicate matching contract

    Current stage:
    - local fingerprint only
    - no external index
    """


    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}


        fingerprint = self.build_fingerprint(
            result
        )


        result["dedup"] = {

            "duplicates": 0,

            "confidence": 0.0,

            "sources": [],

            "canonical_listing": None,

            "fingerprint": fingerprint,

            "status": "fingerprint_ready"
        }


        return result



    def build_fingerprint(
        self,
        result: Dict[str, Any]
    ) -> str:

        city = str(
            result.get(
                "city",
                ""
            )
        ).lower()


        property_type = str(
            result.get(
                "type",
                "apartment"
            )
        ).lower()


        price = str(
            result.get(
                "price",
                0
            )
        )


        market_price = str(
            result.get(
                "market_price",
                0
            )
        )


        raw = "|".join(
            [
                city,
                property_type,
                price,
                market_price,
            ]
        )


        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:16]
