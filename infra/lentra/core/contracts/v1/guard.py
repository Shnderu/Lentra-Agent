from lentra.core.contracts.v1.models.property import Property


def enforce_property_contract(raw: dict) -> Property:

    required = [
        "id",
        "title",
        "price",
        "currency",
        "city",
        "location",
        "source",
    ]

    for field in required:
        if field not in raw:
            raise ValueError(f"[CONTRACT] missing {field}")

    try:
        price = float(raw["price"])
    except Exception:
        raise ValueError("[CONTRACT] invalid price")

    return Property(
        id=str(raw["id"]),
        title=str(raw["title"]),
        price=price,
        currency=str(raw["currency"]),
        city=str(raw["city"]),
        district=str(raw.get("location", "")),
        source=str(raw["source"]),
        raw_text=str(raw.get("raw_text", "")),
        metadata={
            "location": str(raw["location"]),
        },
    )


# Backward compatibility alias.
# Existing callers can migrate gradually.
enforce_listing_contract = enforce_property_contract
