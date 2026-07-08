from typing import Dict, Any, List


class DedupIndex:
    """
    Local Deduplication Index.

    Responsibility:
    - store listing fingerprints
    - find similar objects
    - provide duplicate context

    Current stage:
    - in-memory index
    - later replaceable by persistent storage
    """

    def __init__(self):

        self.records: Dict[str, Dict[str, Any]] = {}


    def register(
        self,
        fingerprint: str,
        listing: Dict[str, Any]
    ):

        if fingerprint not in self.records:

            self.records[fingerprint] = {
                "canonical_listing": listing.get(
                    "id"
                ),
                "sources": [],
                "items": []
            }


        source = listing.get(
            "source",
            "unknown"
        )


        if source not in self.records[fingerprint]["sources"]:
            self.records[fingerprint]["sources"].append(
                source
            )


        self.records[fingerprint]["items"].append(
            listing
        )


    def find(
        self,
        fingerprint: str
    ) -> Dict[str, Any]:

        record = self.records.get(
            fingerprint
        )


        if not record:

            return {
                "duplicates": 0,
                "confidence": 0.0,
                "sources": [],
                "canonical_listing": None
            }


        count = len(
            record["items"]
        )


        confidence = 0.0

        if count > 1:
            confidence = min(
                0.95,
                0.5 + (count * 0.15)
            )


        return {

            "duplicates": max(
                count - 1,
                0
            ),

            "confidence": round(
                confidence,
                2
            ),

            "sources": record["sources"],

            "canonical_listing":
                record["canonical_listing"]

        }
