from typing import Dict, Any
import hashlib

from lentra.core.market_intelligence.dedup.dedup_index import DedupIndex


class DedupEngine:
    """
    V3 DEDUP CONTRACT

    Responsibility:
    - create fingerprint
    - register listings
    - detect duplicates
    """

    def __init__(self):

        self.index = DedupIndex()


    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(result, dict):
            result = {}


        fingerprint = self.build_fingerprint(
            result
        )


        self.index.register(
            fingerprint,
            result
        )


        duplicate_context = self.index.find(
            fingerprint
        )


        result["dedup"] = {

            **duplicate_context,

            "fingerprint": fingerprint,

            "status": "index_checked"

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


        title = str(
            result.get(
                "title",
                ""
            )
        ).lower()


        price = str(
            result.get(
                "price",
                0
            )
        )


        raw = "|".join(
            [
                city,
                property_type,
                title,
                price,
            ]
        )


        return hashlib.sha256(
            raw.encode(
                "utf-8"
            )
        ).hexdigest()[:16]
