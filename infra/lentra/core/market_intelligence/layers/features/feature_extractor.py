from lentra.core.contracts.v1.models.property import Property


def extract_features(property: Property) -> dict:
    return {
        "price": property.price,
        "city": property.city,
        "location": property.district
        or property.metadata.get("location", ""),
        "currency": property.currency,
        "title_length": len(property.title or ""),
        "is_near_beach": "beach" in (property.title or "").lower(),
    }
