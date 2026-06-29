from typing import Any, Dict


class SafeNormalizer:

    @staticmethod
    def normalize_location(location: Any) -> Dict[str, str]:

        if isinstance(location, dict):
            return {
                "segment": location.get("segment", "unknown"),
                "micro_market": location.get("micro_market", "unknown")
            }

        if isinstance(location, str):
            return {
                "segment": location,
                "micro_market": "unknown"
            }

        return {
            "segment": "unknown",
            "micro_market": "unknown"
        }

    @staticmethod
    def normalize_listing(listing: dict) -> dict:

        location = listing.get("location", "unknown")

        listing["location"] = SafeNormalizer.normalize_location(location)

        listing.setdefault("price", 0.0)
        listing.setdefault("risk", 0.5)
        listing.setdefault("confidence", 0.5)

        return listing
