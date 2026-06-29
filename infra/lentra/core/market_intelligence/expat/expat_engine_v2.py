class ExpatEngineV2:

    def process(self, listing: dict) -> dict:

        location = listing.get("location", {})

        if isinstance(location, str):
            segment = location
        else:
            segment = location.get("segment", "unknown")

        if segment in ["beach", "coastal", "premium"]:
            listing["expat_score"] = 0.8
        elif segment in ["city"]:
            listing["expat_score"] = 0.6
        else:
            listing["expat_score"] = 0.4

        return listing
