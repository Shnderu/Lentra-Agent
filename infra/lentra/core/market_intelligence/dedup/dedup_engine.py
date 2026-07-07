from typing import Dict, Any

from lentra.core.market_intelligence.dedup.fingerprint_index import fingerprint_index


class DedupEngine:
    """
    Deduplication Intelligence Engine v1.

    Responsibilities:
    - generate object fingerprint
    - store listing
    - detect existing duplicates
    """


    def evaluate(
        self,
        listing: Dict[str, Any]
    ) -> Dict[str, Any]:

        if not isinstance(listing, dict):
            return {
                "duplicates": 0,
                "confidence": 0.0
            }


        fingerprint = self._fingerprint(
            listing
        )


        existing = fingerprint_index.find(
            fingerprint
        )


        duplicates = len(existing)


        fingerprint_index.add(
            fingerprint,
            listing
        )


        return {
            "fingerprint": fingerprint,
            "duplicates": duplicates,
            "confidence": (
                0.9
                if duplicates
                else 0.0
            ),
            "sources": [
                x.get("source")
                for x in existing
            ],
            "status": (
                "duplicate_found"
                if duplicates
                else "new_listing"
            )
        }


    def _fingerprint(
        self,
        listing: Dict[str, Any]
    ) -> str:

        title = listing.get(
            "title",
            ""
        ).lower()

        city = listing.get(
            "city",
            ""
        )

        normalized = (
            title
            .replace("studio", "")
            .replace("apartment", "")
            .replace("near", "")
            .replace(" ", "")
            +
            city
        )

        import hashlib

        return hashlib.sha256(
            normalized.encode()
        ).hexdigest()[:16]
