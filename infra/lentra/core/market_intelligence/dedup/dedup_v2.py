import hashlib
from typing import Dict, Set, List


class DedupV2Engine:
    """
    Contract v2:
    - analyze(listings) -> deduplicated listings
    - internal signature store
    """

    def __init__(self):
        self.signatures: Set[str] = set()

    def build_global_signature(self, listing: Dict) -> str:
        base = f"{listing.get('city')}::{listing.get('location')}::{listing.get('price')}::{listing.get('title')}"
        return hashlib.sha256(base.encode()).hexdigest()

    def is_duplicate(self, listing: Dict) -> bool:
        sig = self.build_global_signature(listing)
        return sig in self.signatures

    def register(self, listing: Dict):
        sig = self.build_global_signature(listing)
        self.signatures.add(sig)

    def analyze(self, listings: List[Dict]) -> List[Dict]:
        result = []

        for item in listings:
            if not self.is_duplicate(item):
                self.register(item)
                item["is_duplicate"] = False
                result.append(item)
            else:
                item["is_duplicate"] = True

        return result
