class AreaEngineV2:

    def process(self, listing: dict) -> dict:

        location = listing.get("location", {})

        if isinstance(location, str):
            segment = location
        else:
            segment = location.get("segment", "unknown")

        # SINGLE SOURCE OF TRUTH FOR SEGMENTS

        mapping = {
            "beach": "coastal_premium",
            "city": "urban_core",
            "suburb": "residential",
        }

        listing["location"] = {
            "segment": segment,
            "micro_market": mapping.get(segment, "unknown")
        }

        return listing
