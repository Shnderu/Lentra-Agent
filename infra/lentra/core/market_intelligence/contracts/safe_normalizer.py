from typing import List, Dict, Any


class SafeNormalizer:

    def normalize_listing(self, listing: Dict[str, Any]) -> Dict[str, Any]:
        """
        GUARANTEES BASE STRUCTURE
        """
        return {
            "title": listing.get("title", ""),
            "price": listing.get("price", 0),
            "city": listing.get("city"),
            "location": listing.get("location")
        }

    def normalize_batch(self, listings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.normalize_listing(l) for l in listings]
