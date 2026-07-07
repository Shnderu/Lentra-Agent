from typing import Dict, Any, List


class FingerprintIndex:
    """
    Deduplication fingerprint storage.

    Phase 1:
    - in-memory index
    - fingerprint matching
    - duplicate discovery

    Future:
    - persistent storage
    - vector similarity
    - source reconciliation
    """

    def __init__(self):
        self._index: Dict[str, List[Dict[str, Any]]] = {}

    def add(
        self,
        fingerprint: str,
        listing: Dict[str, Any]
    ):
        if not fingerprint:
            return

        if fingerprint not in self._index:
            self._index[fingerprint] = []

        self._index[fingerprint].append(
            listing
        )

    def find(
        self,
        fingerprint: str
    ) -> List[Dict[str, Any]]:

        if not fingerprint:
            return []

        return self._index.get(
            fingerprint,
            []
        )

    def count(
        self,
        fingerprint: str
    ) -> int:

        return len(
            self.find(fingerprint)
        )

    def snapshot(self):
        return self._index.copy()


fingerprint_index = FingerprintIndex()
