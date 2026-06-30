class DemandHeatmapEngineV1:

    def enrich(self, listing):

        location = listing.get("location", {})

        if isinstance(location, str):
            segment = location
        else:
            segment = location.get("segment", "unknown")

        demand_map = {
            "beach": 0.9,
            "city": 1.0,
            "suburb": 0.6,
            "unknown": 0.5
        }

        demand = demand_map.get(segment, 0.5)

        listing["demand"] = {
            "score": demand,
            "heat": "high" if demand > 0.85 else "medium" if demand > 0.6 else "low"
        }

        return listing
