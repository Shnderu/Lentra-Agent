from lentra.core.contracts.v1.models.listing import Listing


def extract_features(listing: Listing) -> dict:
    return {
        "price": listing.price,
        "city": listing.city,
        "location": listing.location,
        "currency": listing.currency,
        "title_length": len(listing.title or ""),
        "is_near_beach": "beach" in (listing.title or "").lower(),
    }
