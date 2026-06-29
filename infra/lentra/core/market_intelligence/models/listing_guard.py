class ListingGuard:

    @staticmethod
    def ensure(obj: dict) -> dict:
        if not isinstance(obj, dict):
            obj = {}

        return {
            "title": obj.get("title"),
            "price": obj.get("price"),
            "location": obj.get("location"),
            "photos": obj.get("photos") or [],

            "area_quality": obj.get("area_quality"),
            "risk": obj.get("risk"),
            "price_deviation": obj.get("price_deviation"),

            "score": obj.get("score"),
            "verdict": obj.get("verdict"),
            "confidence": obj.get("confidence"),

            "source": obj.get("source"),
            "currency": obj.get("currency"),
        }
