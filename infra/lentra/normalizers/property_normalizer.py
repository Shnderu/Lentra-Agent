from lentra.property.models import Property


class PropertyNormalizer:

    @staticmethod
    def normalize(raw: dict, source: str) -> Property:

        return Property(
            id=str(raw.get("id")),
            source=source,
            title=raw.get("title", ""),
            url=raw.get("url", ""),
            city=raw.get("city", ""),
            district=raw.get("district"),
            price=float(raw.get("price", 0)),
            bedrooms=raw.get("bedrooms"),
            bathrooms=raw.get("bathrooms"),
            lat=raw.get("lat"),
            lng=raw.get("lng"),
            trust_score=float(raw.get("trust_score", 50)),
            photos=raw.get("photos", []),
            metadata=raw,
        )
