class SourceFusionEngineV1:

    def merge(self, listings):

        # v1 simple dedup + confidence boost
        seen = {}
        result = []

        for l in listings:

            key = (
                l.get("price"),
                str(l.get("location"))
            )

            if key in seen:
                # merge signals
                existing = seen[key]
                existing["confidence"] = min(1.0, existing.get("confidence", 0.5) + 0.1)
            else:
                l["confidence"] = l.get("confidence", 0.5)
                seen[key] = l
                result.append(l)

        return result
