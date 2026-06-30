

class GeoIntelligenceEngineV1:

    def enrich(self, listing):

        location = listing.get("location", {})

        if isinstance(location, str):
            segment = location
        else:
            segment = location.get("segment", "unknown")

        # simple geo classification v1
        mapping = {
            "beach": {
                "zone": "coastal",
                "demand": 0.9,
                "liquidity": 0.7
            },
            "city": {
                "zone": "urban",
                "demand": 1.0,
                "liquidity": 0.9
            }
        }

        geo = mapping.get(segment, {
            "zone": "unknown",
            "demand": 0.5,
            "liquidity": 0.5
        })

        listing["geo"] = geo

        return listing
