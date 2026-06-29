class ListingNormalizer:

    def normalize(self, listing: dict) -> dict:

        # safe defaults
        return {
            "title": listing.get("title", ""),
            "price": float(listing.get("price", 0) or 0),
            "location": listing.get("location", ""),
            "photos": listing.get("photos", []),
            "source": listing.get("source", "unknown"),
            "currency": listing.get("currency", "USD")
        }
