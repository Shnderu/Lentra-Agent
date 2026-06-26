from lentra.core.models.listing import Listing


def normalize(listings: list) -> list:
    normalized = []

    for x in listings:
        listing = Listing(
            id=x.get("id"),
            title=x.get("title"),
            price=float(x.get("price", 0)),
            currency=x.get("currency", "USD"),
            location=x.get("location", ""),
            source=x.get("source", "unknown"),
            normalized_price=float(x.get("price", 0))
        )

        normalized.append(listing)

    return normalized
