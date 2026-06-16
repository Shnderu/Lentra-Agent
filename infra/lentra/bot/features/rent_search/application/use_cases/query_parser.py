from lentra.bot.features.rent_search.application.dto.search_query import NormalizedRentQuery


class RentQueryParser:
    """
    MVP parser: rule-based extraction layer.
    Later can be replaced with LLM / NLP model.
    """

    def parse(self, text: str) -> NormalizedRentQuery:
        t = (text or "").lower()

        city = None
        if "vietnam" in t or "вьетнам" in t:
            city = "Vietnam"

        property_type = None
        if "room" in t:
            property_type = "room"
        elif "house" in t:
            property_type = "house"
        elif "apartment" in t or "flat" in t or "квартира" in t:
            property_type = "apartment"

        min_price = None
        max_price = None

        # very simple heuristic
        if "cheap" in t or "дешев" in t:
            max_price = 500

        if "lux" in t or "luxury" in t:
            min_price = 1000

        return NormalizedRentQuery(
            raw_text=text,
            city=city,
            min_price=min_price,
            max_price=max_price,
            property_type=property_type,
        )
