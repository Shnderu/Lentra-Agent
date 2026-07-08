from typing import Dict, Any
import hashlib

from lentra.core.market_intelligence.dedup.dedup_index import DedupIndex


class DedupEngine:


    def __init__(self):

        self.index = DedupIndex()



    def evaluate(
        self,
        result: Dict[str, Any]
    ) -> Dict[str, Any]:

        fingerprint = self.build_fingerprint(
            result
        )


        result["fingerprint"] = fingerprint


        self.index.register(
            result
        )


        context = self.index.analyze(
            result
        )


        result["dedup"] = {

            **context,

            "fingerprint": fingerprint,

            "status": "memory_checked"

        }


        return result



    def build_fingerprint(
        self,
        result: Dict[str, Any]
    ) -> str:

        raw = "|".join(
            [
                str(result.get("city","")),
                str(result.get("type","")),
                str(result.get("title","")).lower()
            ]
        )


        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:16]
