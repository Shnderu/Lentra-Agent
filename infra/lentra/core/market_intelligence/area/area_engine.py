class AreaEngine:

    def evaluate(self, listing: dict) -> dict:

        location = (listing.get("location") or "").lower()

        base = 5.5

        if "beach" in location:
            base = 8.0
        elif "center" in location:
            base = 6.0
        elif "suburb" in location:
            base = 4.5

        return {
            "area_quality": base
        }
