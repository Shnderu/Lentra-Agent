from lentra.core.contracts.v1.models.listing import Listing


def enforce_listing_contract(raw: dict) -> Listing:

    required = ["id", "title", "price", "currency", "city", "location", "source"]

    for r in required:
        if r not in raw:
            raise ValueError(f"[CONTRACT] missing {r}")

    try:
        price = float(raw["price"])
    except Exception:
        raise ValueError("[CONTRACT] invalid price")

    return Listing(
        id=str(raw["id"]),
        title=str(raw["title"]),
        price=price,
        currency=str(raw["currency"]),
        city=str(raw["city"]),
        location=str(raw["location"]),
        source=str(raw["source"]),
    )
